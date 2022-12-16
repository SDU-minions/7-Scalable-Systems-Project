package com.example.scalablesystems

import java.sql.Connection
import java.sql.DriverManager



object HiveConnection{

    //@JvmStatic
    public fun connect() {
        var con: Connection? = null
        try {
            //val conStr = "jdbc:hive2://192.168.1.148:10000/default"
            val conStr = "jdbc:hive2://localhost:10000"
            Class.forName("org.apache.hive.jdbc.HiveDriver")
            con = DriverManager.getConnection(conStr, "hive", "hive")
            val stmt = con.createStatement()
            stmt.executeQuery("show tables")
            println("show database successfully.")
        } catch (ex: Exception) {
            ex.printStackTrace()
        } finally {
            try {
                con?.close()
            } catch (ex: Exception) {
            }
        }
    }

}