import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import TypeAlias

Json: TypeAlias = None | bool | int | float | str | list["Json"] | dict[str, "Json"]
REPOSITORY = "kirill-markin/nibomo-plugins"
APP = "app_741c52b8-681c-4e8c-8536-9b278e02d671"
PACKAGE = "@nibomo/nibomo"
HOST = "https://v2.executor.sh"
SOURCE_PATHS = ["LICENSE", "README.md", "index.ts", "package.json", "provider.ts"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def record(value: Json) -> dict[str, Json]:
    if not isinstance(value, dict):
        raise ValueError("Expected a JSON object")
    return value


def items(value: Json) -> list[Json]:
    if not isinstance(value, list):
        raise ValueError("Expected a JSON array")
    return value


def string(value: Json) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("Expected a nonempty JSON string")
    return value


def commit(value: Json) -> str:
    result = string(value)
    require(re.fullmatch(r"[a-f0-9]{40}", result) is not None, "Expected a full immutable Git commit")
    return result


def environment(name: str) -> str:
    value = os.environ.get(name, "")
    require(bool(value), f"Missing {name}; configure the workflow secret/input before retrying")
    return value


def note(label: str, value: str) -> None:
    with Path(environment("GITHUB_STEP_SUMMARY")).open("a") as summary:
        summary.write(f"- {label}: {value}\n")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url: str, token: str, method: str, body: Json) -> Json:
    headers = {"Accept": "application/json", "User-Agent": "nibomo-executor-publisher"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    payload = None if body is None else json.dumps(body).encode()
    if payload is not None:
        headers["Content-Type"] = "application/json"
    # Never forward credentials or redirect a mutation to another endpoint.
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(urllib.request.Request(url, payload, headers, method=method), timeout=180) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        if token:
            detail = detail.replace(token, "[redacted]")
        raise RuntimeError(f"{method} {url}: HTTP {error.code}: {detail[:2000]}") from None
    except urllib.error.URLError as error:
        raise RuntimeError(f"{method} {url}: {error.reason}; inspect remote state before retrying") from None


def github(path: str) -> Json:
    return request(f"https://api.github.com/repos/{REPOSITORY}/{path}", environment("GITHUB_TOKEN"), "GET", None)


def executor(path: str, method: str, body: Json) -> Json:
    return request(f"{HOST}{path}", environment("EXECUTOR_API_TOKEN"), method, body)


def git(*arguments: str) -> str:
    return subprocess.check_output(["git", *arguments]).decode("utf-8")


def source(sha: str) -> dict[str, str]:
    entries = git("ls-tree", "-r", sha, "--", "executor/").splitlines()
    paths = []
    for entry in entries:
        metadata, path = entry.split("\t", 1)
        require(metadata.startswith("100644 blob "), f"Unexpected source file mode: {path}")
        paths.append(path.removeprefix("executor/"))
    require(sorted(paths) == SOURCE_PATHS, f"Unexpected executor source set at {sha}: {paths}; reconcile SOURCE_PATHS explicitly")
    return {path: git("show", f"{sha}:executor/{path}") for path in SOURCE_PATHS}


def files(value: Json) -> dict[str, str]:
    result: dict[str, str] = {}
    for entry in items(value):
        data = record(entry)
        path = string(data["path"])
        require(path not in result, f"Duplicate remote source path: {path}")
        content = data["content"]
        if not isinstance(content, str):
            raise ValueError(f"Incomplete remote source: {path}")
        result[path] = content
    require(sorted(result) == SOURCE_PATHS, f"Unexpected remote source set: {sorted(result)}; reconcile before deleting or omitting files")
    return result


def publication(value: Json) -> str:
    data = record(value)
    require(data["name"] == PACKAGE, "Unexpected public package identity")
    return commit(data["commit"])


def listing(value: Json) -> dict[str, Json]:
    matches = [record(item) for item in items(value) if record(item)["name"] == PACKAGE]
    require(len(matches) == 1, "Expected exactly one existing @nibomo/nibomo listing; never create a replacement")
    return matches[0]


def release_sha(tag: str) -> str:
    release = record(github(f"releases/tags/{tag}"))
    require(release["tag_name"] == tag and release["draft"] is False and release["prerelease"] is False,
            "Only an existing published stable release is allowed")
    ref = record(record(github(f"git/ref/tags/{tag}"))["object"])
    while ref["type"] == "tag":
        ref = record(record(github(f"git/tags/{commit(ref['sha'])}"))["object"])
    require(ref["type"] == "commit", "Release tag must resolve to a commit")
    sha = commit(ref["sha"])
    require(git("rev-parse", f"refs/tags/{tag}^{{commit}}").strip() == sha, "Release tag changed since checkout")
    if tag == "v1.29.0":
        require(sha == "41cd84f6f8b947131dbbca36b6f8a577db1f1993", "Immutable v1.29.0 tag moved")
    subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], check=True)
    for path in ["plugin.json", ".claude-plugin/plugin.json", "gemini-extension.json"]:
        manifest = record(json.loads(git("show", f"{sha}:{path}")))
        require(manifest["name"] == "nibomo" and manifest["version"] == tag[1:], f"Release/manifest mismatch: {path}")
    return sha


def cloud_run(sha: str) -> str:
    data = record(github(f"actions/workflows/packages.yml/runs?head_sha={sha}&event=push&branch=main&per_page=100"))
    runs = [record(item) for item in items(data["workflow_runs"])]
    require(bool(runs), f"No Plugin packages main push run for {sha}")
    run = runs[0]
    require(run["head_sha"] == sha and run["head_branch"] == "main" and run["event"] == "push"
            and run["name"] == "Plugin packages" and run["status"] == "completed" and run["conclusion"] == "success",
            f"Latest exact-SHA Plugin packages run is not successful: {run['html_url']}")
    jobs = record(github(f"actions/runs/{run['id']}/jobs?per_page=100"))
    entries = items(jobs["jobs"])
    require(jobs["total_count"] == len(entries), "Unexpected job pagination; inspect cloud run")
    for name in ["packages", "Executor typecheck"]:
        matches = [record(job) for job in entries if record(job)["name"] == name]
        require(len(matches) == 1 and matches[0]["conclusion"] == "success", f"Required cloud job not successful: {name}")
    return string(run["html_url"])


def selections(value: Json) -> dict[str, dict[str, Json]]:
    result: dict[str, dict[str, Json]] = {}
    for value in items(value):
        profile = record(value)
        require(profile["app"] == APP, "Unexpected profile app identity")
        accounts = record(profile["accounts"])
        for account in accounts.values():
            if isinstance(account, list):
                for identifier in account:
                    string(identifier)
            else:
                string(account)
        identifier = string(profile["id"])
        require(identifier not in result, "Duplicate profile identity")
        result[identifier] = accounts
    return result


def main() -> None:
    environment("EXECUTOR_API_TOKEN")
    require(environment("GITHUB_REPOSITORY") == REPOSITORY, "Wrong GitHub repository")
    event_name = environment("GITHUB_EVENT_NAME")
    require(event_name in ["release", "workflow_dispatch"], "Publication requires a release or manual retry")
    event = record(json.loads(Path(environment("GITHUB_EVENT_PATH")).read_text()))
    if event_name == "release":
        require(event["action"] == "published", "Expected release published event")
        tag = string(record(event["release"])["tag_name"])
    else:
        require(environment("GITHUB_REF") == "refs/heads/main", "Run manual retries from main")
        tag = environment("RELEASE_TAG")
    require(re.fullmatch(r"v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", tag) is not None,
            "release_tag must be an existing stable vX.Y.Z release")
    sha = release_sha(tag)
    note("GitHub release", f"[{tag}](https://github.com/{REPOSITORY}/releases/tag/{tag}) — {sha}")
    note("Publisher SHA", git("rev-parse", "HEAD").strip())
    note("Plugin packages", cloud_run(sha))
    intended = source(sha)
    require(record(json.loads(intended["package.json"]))["name"] == PACKAGE, "Wrong Executor package name")
    context = record(executor("/api/context?organization=nibomo", "GET", None))
    require(context["slug"] == "nibomo" and context["role"] in ["owner", "admin"], "Nibomo owner/admin access required")
    base = f"/api/organizations/{urllib.parse.quote(string(context['organization']), safe='')}"
    access = record(executor(f"{base}/access", "GET", None))
    require(access["organization"] == context["organization"] and access["role"] == context["role"], "Organization access changed")
    app_path = f"{base}/apps/{APP}"
    app = record(executor(app_path, "GET", None))
    require(app["id"] == APP and app["owner"] == access["owner"] and app["slug"] == "nibomo", "Unexpected owned app identity")
    authoring = record(executor(f"{app_path}/authoring", "GET", None))
    require(authoring["namespace"] == "nibomo" and authoring["canEdit"] is True and authoring["canPublish"] is True,
            "Existing app edit/publish permissions required")
    working = record(executor(f"{app_path}/workspace", "GET", None))
    revision = record(working["revision"])
    working_commit = commit(revision["commit"])
    require(revision["code"] == app["repository"] and working["namespace"] == "nibomo" and working["canEdit"] is True,
            "Unexpected working source identity or permissions")
    current = files(working["files"])
    deployed = record(executor(f"{app_path}/source", "GET", None))
    require(deployed["id"] == app["activeDeployment"] and deployed["code"] == app["code"]
            and deployed["owner"] == access["owner"], "Unexpected active deployment identity")
    public_path = "/api/registry/apps?name=%40nibomo%2Fnibomo"
    published = listing(executor(f"{base}/app-publications/published", "GET", None))
    published_commit = publication(published)
    public = listing(request(f"{HOST}{public_path}", "", "GET", None))
    require(publication(public) == published_commit, "Owned and public listings disagree before publication")
    snapshot = record(request(f"{HOST}/api/registry/source?name=%40nibomo%2Fnibomo&commit={published_commit}", "", "GET", None))
    require(publication(snapshot["publication"]) == published_commit, "Unexpected public source identity")
    files(snapshot["files"])
    before_accounts = selections(executor(f"{app_path}/profiles", "GET", None))
    if current != intended:
        require(working_commit == deployed["sourceCommit"] == published_commit
                and current == files(deployed["files"]) == files(snapshot["files"]),
                "Remote working/deployed/public source drift; reconcile explicitly before retrying")
        history = git("log", "--first-parent", "--format=%H", "HEAD", "--", "executor/").splitlines()
        require(any(source(previous) == current for previous in history),
                "Remote source does not match reviewed main ancestry; reconcile explicitly before retrying")
        require(release_sha(tag) == sha, "Release tag changed before publication")
        saved = record(executor(f"{app_path}/commits", "POST", {
            "expected": working_commit,
            "files": [{"path": path, "content": content} for path, content in intended.items()],
            "message": f"Publish Nibomo {tag} from {sha}",
        }))
        saved_revision = record(saved["revision"])
        require(saved_revision["code"] == revision["code"] and files(saved["files"]) == intended, "Saved source mismatch")
        working_commit = commit(saved_revision["commit"])
    else:
        require(release_sha(tag) == sha, "Release tag changed before publication")
    note("Executor source commit", working_commit)
    unchanged = deployed["sourceCommit"] == working_commit and published_commit == working_commit
    if deployed["sourceCommit"] != working_commit:
        result = record(executor(f"{app_path}/deploy", "POST", {"commit": working_commit}))
        deployed = record(result["deployment"])
        returned_app = record(result["app"])
        require(returned_app["id"] == APP and returned_app["owner"] == access["owner"]
                and returned_app["activeDeployment"] == deployed["id"], "Deployment response app mismatch")
    require(deployed["sourceCommit"] == working_commit and files(deployed["files"]) == intended, "Deployment source mismatch")
    note("Deployment", f"{string(deployed['id'])} — commit {working_commit}")
    active = record(executor(app_path, "GET", None))
    verified = record(executor(f"{app_path}/source", "GET", None))
    require(active["activeDeployment"] == deployed["id"] == verified["id"] and verified["sourceCommit"] == working_commit
            and verified["owner"] == access["owner"] and files(verified["files"]) == intended, "Active deployment verification failed")
    require(selections(executor(f"{app_path}/profiles", "GET", None)) == before_accounts, "Account selections changed; inspect before publication")
    latest_working = record(executor(f"{app_path}/workspace", "GET", None))
    require(record(latest_working["revision"])["commit"] == working_commit and files(latest_working["files"]) == intended,
            "Working source changed during deployment; reconcile before publication")
    if published_commit != working_commit:
        accepted = executor(f"{app_path}/publication", "POST", {"commit": working_commit})
        require(publication(accepted) == working_commit, "Accepted publication identity mismatch")
        note("Publication accepted", f"{PACKAGE} — {working_commit}")
    owned = listing(executor(f"{base}/app-publications/published", "GET", None))
    require(publication(owned) == working_commit, "Publication readback mismatch")
    visible = items(request(f"{HOST}{public_path}", "", "GET", None))
    if not visible:
        note("Public listing", "Propagation pending; accepted publication verified, repeat the manual workflow to recheck")
    else:
        require(publication(listing(visible)) == working_commit, "Immediate public listing commit mismatch; inspect provider state")
        live = record(request(f"{HOST}/api/registry/source?name=%40nibomo%2Fnibomo&commit={working_commit}", "", "GET", None))
        require(publication(live["publication"]) == working_commit and files(live["files"]) == intended, "Public source mismatch")
        note("Public listing", "[Verified source](https://v2.executor.sh/apps/nibomo/nibomo)")
    note("Outcome", "No update needed" if unchanged and visible else "Operator-complete: deployment and accepted publication verified")
    note("Installed copies", "Remain independent; users must review and install the new source")


if __name__ == "__main__":
    main()
