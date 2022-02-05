package io.github.iskandergaba.java;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class TSDBDropper {

    public static void main(String... args) {
        final var db = "jdbc:postgresql://localhost:8812/qdb";
        final var user = "admin";
        final var pwd = "quest";

        System.out.println("Dropping tables from `qdb` database...");
        try (var conn = DriverManager.getConnection(db, user, pwd)) {
            dropSchema(conn);
        } catch (SQLException ex) {
            System.err.println(ex.getMessage());
        }
        System.out.println("Done.");


    }

    private static void dropSchema(final Connection conn) throws SQLException {
        try (var stmt = conn.createStatement()) {
            stmt.execute("DROP TABLE sys_load;");
            stmt.execute("DROP TABLE sys_load_hourly;");
        }
    }
}
