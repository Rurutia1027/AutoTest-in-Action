import pytest
from src.fixtures.prometheus_fixtures import query_prometheus


@pytest.mark.functional
@pytest.mark.prometheus
class TestPrometheusPostgresMetrics:
    """
    Test suite for PostgreSQL metrics exposed via postgres-exporter in Prometheus.
    """
    states = [
        "active",
        "disabled",
        "fastpath function call",
        "idle",
        "idle in transaction",
        "idle in transaction (aborted)"
    ]

    def test_pg_stat_activity_count_labels(self, query_prometheus):
        """
        Verify pg_stat_activity_count exists for all states in the existing databases.
        Dynamically discover databases from the metric result.
        """
        resp = query_prometheus("pg_stat_activity_count")
        databases = set([m["metric"]["datname"] for m in resp["data"]["result"]])

        for db in databases:
            for state in self.states:
                filtered = [
                    m for m in resp["data"]["result"]
                    if m["metric"]["datname"] == db and m["metric"]["state"] == state
                ]
                assert filtered, f"Metric missing for db={db}, state={state}"
                value = float(filtered[0]["value"][1])
                assert value >= 0, f"Metric value negative for db={db}, state={state}"

    def test_pg_up_metric(self, query_prometheus):
        """
        Verify the 'up' metric for the postgres job.
        """
        resp = query_prometheus("up")
        filtered = [m for m in resp["data"]["result"] if m["metric"].get("job") == "postgres"]
        assert filtered, "No 'up' metric found for postgres job"
        value = float(filtered[0]["value"][1])
        assert value == 1, "Postgres exporter not up"

    def test_pg_stat_activity_count_total(self, query_prometheus):
        """
        Verify total activity count per database is non-negative.
        """
        resp = query_prometheus("pg_stat_activity_count")
        databases = set([m["metric"]["datname"] for m in resp["data"]["result"]])

        for db in databases:
            total = sum(
                float(m["value"][1])
                for m in resp["data"]["result"]
                if m["metric"]["datname"] == db
            )
            assert total >= 0, f"Total activity count should be non-negative for db={db}"
