package io.github.iskandergaba.java;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class TSDBCreator {

    public static void main(String... args) {
        final var db = "jdbc:postgresql://localhost:8812/qdb";
        final var user = "admin";
        final var pwd = "quest";

        System.out.println("Creating tables in `qdb` database...");
        // Create database
        try (var conn = DriverManager.getConnection(db, user, pwd)) {
            createSchema(conn);
            insertData(conn);
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
                    CREATE TABLE IF NOT EXISTS sys_load (
                        time TIMESTAMP,
                        cpu_load DOUBLE PRECISION,
                        memory_usage DOUBLE PRECISION,
                        network_usage DOUBLE PRECISION
                        ) timestamp(time) PARTITION BY MONTH;
                    """);
        }

        try (var stmt = conn.createStatement()) {
            stmt.execute("""
                    CREATE TABLE IF NOT EXISTS sys_load_hourly (
                        time TIMESTAMP,
                        cpu_load DOUBLE PRECISION,
                        memory_usage DOUBLE PRECISION,
                        network_usage DOUBLE PRECISION
                        ) timestamp(time) PARTITION BY MONTH;
                    """);
        }
    }

    private static void insertData(final Connection conn) throws SQLException {
        try (var stmt = conn.prepareStatement("""
                INSERT INTO sys_load
                    SELECT
                        timestamp_sequence(to_timestamp('2021-01-01T00:00:00', 'yyyy-MM-ddTHH:mm:ss'), 1000000L),
                        rnd_double(0),
                        rnd_double(0),
                        rnd_double(0)
                    FROM long_sequence(31550000);
                """)) {
            stmt.executeUpdate();
        }

        try (var stmt = conn.prepareStatement("""
                INSERT INTO sys_load_hourly
                    SELECT
                        time,
                        avg(cpu_load) cpu_load,
                        avg(memory_usage) memory_usage,
                        avg(network_usage) network_usage
                    FROM sys_load SAMPLE BY 1h;
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
        // Get the first 24 hours of aggregation
        try (var stmt = conn.prepareStatement("""
                SELECT *
                FROM sys_load_hourly
                ORDER BY time ASC
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
