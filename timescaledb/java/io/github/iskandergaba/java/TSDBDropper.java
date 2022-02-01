package io.github.iskandergaba.java;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class TSDBDropper {

    public static void main(String... args) {
        final var db = "jdbc:postgresql://localhost:5432/metrics";
        final var user = "postgres";
        final var pwd = "root";

        System.out.println("Dropping tables and views from `metrics` database...");
        try (var conn = DriverManager.getConnection(db, user, pwd)) {
            dropSchema(conn);
        } catch (SQLException ex) {
            System.err.println(ex.getMessage());
        }
        System.out.println("Done.");


    }

    private static void dropSchema(final Connection conn) throws SQLException {
        try (var stmt = conn.createStatement()) {
            stmt.execute("DROP MATERIALIZED VIEW IF EXISTS sys_load_hourly;");
            stmt.execute("DROP TABLE IF EXISTS sys_load;");
        }
    }
}
