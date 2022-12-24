import requests
from playwright.sync_api import Page, expect
from tests.fixtures import url
from tests.fixtures.monitoring_user import *
from tests.nav.monitoring.grafana.dashboards import (
    go_to_dashboard_from_search,
    nav_to_dashboards,
)
from tests.nav.monitoring.grafana.datasources import (
    navigate_to_cloudwatch_data_source_and_test,
    navigate_to_prometheus_data_source_and_test,
)
from tests.nav.monitoring.grafana.panels import locate_panel_by_name


def test_grafana_loads():
    resp = requests.get(url.monitoring(), verify=False)
    assert resp.status_code == 200
    assert "Grafana" in resp.text


def test_prometheus_connected_to_grafana(page: Page, monitoring_user):
    navigate_to_prometheus_data_source_and_test(page)
    nav_to_dashboards(page)
    go_to_dashboard_from_search(page, "API ALB")
    expect(locate_panel_by_name(page, "2xx Response Count")).to_contain_text(
        "httpcode",
        timeout=10000,
    )


def test_cloudwatch_connected_to_grafana(page: Page, monitoring_user):
    navigate_to_cloudwatch_data_source_and_test(page)
    nav_to_dashboards(page)
    go_to_dashboard_from_search(page, "Amazon CloudWatch Logs")
    expect(
        locate_panel_by_name(page, "Incoming log events [count/sec]")
    ).to_contain_text(
        "ecs",
    )
