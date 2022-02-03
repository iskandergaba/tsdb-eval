package io.github.iskandergaba.java;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class TSDBCreator {

    public static void main(String... args) {
        final var db = "jdbc:postgresql://localhost:5432/metrics";
        final var user = "postgres";
        final var pwd = "root";

        System.out.println("Creating tables in `metrics` database...");
        // Create database
        try (var conn = DriverManager.getConnection(db, user, pwd)) {
            createSchema(conn);
            insertData(conn);
            setPolicies(conn);
        } catch (SQLException ex) {
            System.err.println(ex.getMessage());
        }
        System.out.println("Done.");

        // Check results
        try (var conn = DriverManager.getConnection(db, user, pwd)) {
            executeQueries(conn);
        } catch (SQLException ex) {
            System.err.println(ex.getMessage());
        }
    }

    private static void createSchema(final Connection conn) throws SQLException {

        // Create table sys_load
        try (var stmt = conn.createStatement()) {
            stmt.execute("""
                    CREATE TABLE sys_load (
                        time TIMESTAMPTZ NOT NULL,
                        cpu_load DOUBLE PRECISION,
                        memory_usage DOUBLE PRECISION,
                        network_usage DOUBLE PRECISION
                    )
                    """);
        }

        // Convert sys_load to TimeScaleDB hypertable
        try (var stmt = conn.createStatement()) {
            stmt.execute("SELECT create_hypertable('sys_load', 'time')");
        }

        // Create hourly average view sys_load_hourly
        try (var stmt = conn.createStatement()) {
            stmt.execute("""
                    CREATE MATERIALIZED VIEW sys_load_hourly
                    WITH (timescaledb.continuous) AS
                    SELECT time_bucket(INTERVAL '1 hour', time) AS bucket,
                       AVG(cpu_load) AS cpu_load,
                       AVG(memory_usage) AS memory_usage,
                       AVG(network_usage) AS network_usage
                    FROM sys_load
                    GROUP BY bucket
                    """);
        }
    }

    private static void setPolicies(final Connection conn) throws SQLException {
        // Add data retention policy to sys_load
        try (var stmt = conn.createStatement()) {
            stmt.execute("SELECT add_retention_policy('sys_load', INTERVAL '1 week')");
        }

        // Add data retention policy to sys_load_hourly
        try (var stmt = conn.createStatement()) {
            stmt.execute("SELECT add_retention_policy('sys_load_hourly', INTERVAL '1 month')");
        }

        // Add data continuous aggregate policy to sys_load_hourly
        try (var stmt = conn.createStatement()) {
            stmt.execute("""
                    SELECT add_continuous_aggregate_policy('sys_load_hourly',
                    start_offset => INTERVAL '1 month',
                    end_offset => INTERVAL '1 hour',
                    schedule_interval => INTERVAL '1 minute');
                    """);
        }
    }

    private static void insertData(final Connection conn) throws SQLException {

        try (var stmt = conn.prepareStatement("""
                INSERT INTO sys_load (time, cpu_load, memory_usage, network_usage)
                VALUES (
                    generate_series(now() - INTERVAL '1 year', now(), INTERVAL '1 second'),
                    random(),
                    random(),
                    random()
                )
                """)) {
            stmt.executeUpdate();
        }
    }

    private static void executeQueries(final Connection conn) throws SQLException {

        System.out.println("\nsys_load");
        // Get the first 10 data results
        try (var stmt = conn.prepareStatement("""
                SELECT *
                FROM sys_load
                ORDER BY time ASC
                LIMIT 10
                """)) {

            try (var rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.printf("%s: %f, %f, %f%n", rs.getTimestamp(1), rs.getDouble(2), rs.getDouble(3),
                            rs.getDouble(4));
                }
            }
        }

        System.out.println("\nsys_load_hourly");
        // Get the first 24 hours of aggregations
        try (var stmt = conn.prepareStatement("""
                SELECT *
                FROM sys_load_hourly
                ORDER BY bucket ASC
                LIMIT 24
                """)) {
            try (var rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.printf("%s: %f, %f, %f%n", rs.getTimestamp(1), rs.getDouble(2), rs.getDouble(3),
                            rs.getDouble(4));
                }
            }
        }
    }
}
