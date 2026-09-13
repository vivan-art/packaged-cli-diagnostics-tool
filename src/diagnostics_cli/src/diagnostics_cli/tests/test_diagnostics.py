from diagnostics_cli.diagnostics import disk_info, run_diagnostics


def test_successful_diagnostics(tmp_path):
    result = run_diagnostics(str(tmp_path))

    assert result["disk"]["status"] == "ok"
    assert result["python"]["status"] == "ok"
    assert "developer_tools" in result


def test_missing_dependency_is_reported(monkeypatch):
    import diagnostics_cli.diagnostics as module

    monkeypatch.setattr(module.shutil, "which", lambda name: None)

    result = module.developer_tools_info()

    assert all(item["installed"] is False for item in result)
    assert all(item["status"] == "missing" for item in result)


def test_malformed_configuration_path(tmp_path):
    missing = tmp_path / "does-not-exist"

    result = disk_info(str(missing))

    assert result["status"] == "error"
    assert "does not exist" in result["error"]

On Sun, 13 Sept, 2026, 11:39 am Daksh, <dakshc2153@gmail.com> wrote:
from diagnostics_cli.diagnostics import disk_info, run_diagnostics


def test_successful_diagnostics(tmp_path):
    result = run_diagnostics(str(tmp_path))

    assert result["disk"]["status"] == "ok"
    assert result["python"]["status"] == "ok"
    assert "developer_tools" in result


def test_missing_dependency_is_reported(monkeypatch):
    import diagnostics_cli.diagnostics as module

    monkeypatch.setattr(module.shutil, "which", lambda name: None)

    result = module.developer_tools_info()

    assert all(item["installed"] is False for item in result)
    assert all(item["status"] == "missing" for item in result)


def test_malformed_configuration_path(tmp_path):
    missing = tmp_path / "does-not-exist"

    result = disk_info(str(missing))

    assert result["status"] == "error"
    assert "does not exist" in result["error"]
