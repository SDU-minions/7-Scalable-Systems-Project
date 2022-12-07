package com.example.scalablesystems

import java.sql.DriverManager
import java.sql.SQLException


class HiveConnection{/*
    private const val driverName = "org.apache.hadoop.hive.jdbc.HiveDriver"
    @Throws(SQLException::class)
    @JvmStatic
    fun main(args: Array<String>) {
// Register driver and create driver instance
        Class.forName(driverName)
        // get connection
        val con = DriverManager.getConnection("jdbc:hive://localhost:10000/userdb", "", "")
        // create statement
        val stmt = con.createStatement()
        // execute statement
        val res: Resultset = stmt.executeQuery("SELECT * FROM employee WHERE salary>30000;")
        println("Result:")
        println(" ID \t Name \t Salary \t Designation \t Dept ")
        while (res.next()) {
            println(
                res.getInt(1)
                    .toString() + " " + res.getString(2) + " " + res.getDouble(3) + " " + res.getString(
                    4
                ) + " " + res.getString(5)
            )
        }
        con.close()
    }*/
}