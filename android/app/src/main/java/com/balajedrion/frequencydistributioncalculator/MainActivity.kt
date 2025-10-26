package com.balajedrion.frequencydistributioncalculator

import android.graphics.Typeface
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import kotlin.math.ceil
import kotlin.math.log10

class MainActivity : AppCompatActivity() {

    private lateinit var inputEditText: EditText
    private lateinit var calculateButton: Button
    private lateinit var clearButton: Button
    private lateinit var errorText: TextView
    private lateinit var statsCard: CardView
    private lateinit var statsText: TextView
    private lateinit var tableCard: CardView
    private lateinit var resultsTable: TableLayout

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize views
        inputEditText = findViewById(R.id.inputEditText)
        calculateButton = findViewById(R.id.calculateButton)
        clearButton = findViewById(R.id.clearButton)
        errorText = findViewById(R.id.errorText)
        statsCard = findViewById(R.id.statsCard)
        statsText = findViewById(R.id.statsText)
        tableCard = findViewById(R.id.tableCard)
        resultsTable = findViewById(R.id.resultsTable)

        // Set button listeners
        calculateButton.setOnClickListener {
            calculateFrequencyDistribution()
        }

        clearButton.setOnClickListener {
            clearAll()
        }
    }

    private fun calculateFrequencyDistribution() {
        val inputText = inputEditText.text.toString()

        if (inputText.isBlank()) {
            showError("Please enter some data!")
            return
        }

        try {
            // Parse input
            val rawData = inputText.replace(",", " ")
                .split("\\s+".toRegex())
                .filter { it.isNotBlank() }
                .map { it.toDouble() }

            if (rawData.isEmpty()) {
                showError("No valid numbers found!")
                return
            }

            // Hide error
            errorText.visibility = View.GONE

            // Calculate statistics
            val n = rawData.size
            val highest = rawData.maxOrNull()!!
            val lowest = rawData.minOrNull()!!
            val range = highest - lowest

            // Sturges' formula
            val k = ceil(1 + 3.3 * log10(n.toDouble())).toInt()
            val classWidth = ceil(range / k)

            // Display statistics
            displayStatistics(n, highest, lowest, range, k, classWidth)

            // Process frequency distribution
            val classes = mutableListOf<ClassData>()
            var lowerCI = lowest

            while (lowerCI < highest || classes.isEmpty()) {
                val upperCI = lowerCI + classWidth - 1
                val lowerCB = lowerCI - 0.5
                val upperCB = upperCI + 0.5
                val classMark = (lowerCB + upperCB) / 2

                val frequency = rawData.count { it >= lowerCI && it <= upperCI }

                classes.add(
                    ClassData(
                        classInterval = "${lowerCI.toInt()}-${upperCI.toInt()}",
                        classBoundaries = String.format("%.1f-%.1f", lowerCB, upperCB),
                        classMark = classMark,
                        frequency = frequency
                    )
                )

                lowerCI += classWidth
                if (upperCI >= highest) break
            }

            // Calculate cumulative frequencies
            var cumFreq = 0
            val totalFreq = classes.sumOf { it.frequency }

            classes.forEach { classData ->
                cumFreq += classData.frequency
                classData.cumFreqLess = cumFreq
                classData.relFreq = (classData.frequency.toDouble() / totalFreq) * 100
            }

            // Calculate greater than cumulative frequencies
            var cumFreqGreater = totalFreq
            classes.forEach { classData ->
                classData.cumFreqGreater = cumFreqGreater
                cumFreqGreater -= classData.frequency
            }

            // Display table
            displayTable(classes)

        } catch (e: Exception) {
            showError("Invalid input! Please enter numbers only.")
        }
    }

    private fun displayStatistics(n: Int, highest: Double, lowest: Double, range: Double, k: Int, classWidth: Double) {
        statsCard.visibility = View.VISIBLE
        statsText.text = """
            Total: $n  |  Highest: $highest  |  Lowest: $lowest
            Range: $range  |  Classes (K): $k  |  Class Width (C): $classWidth
        """.trimIndent()
    }

    private fun displayTable(classes: List<ClassData>) {
        tableCard.visibility = View.VISIBLE

        // Clear existing rows except header
        val childCount = resultsTable.childCount
        if (childCount > 1) {
            resultsTable.removeViews(1, childCount - 1)
        }

        // Add data rows
        classes.forEach { classData ->
            val row = TableRow(this)
            row.setPadding(0, 8, 0, 8)

            row.addView(createTableCell(classData.classInterval, 70))
            row.addView(createTableCell(classData.classBoundaries, 90))
            row.addView(createTableCell(String.format("%.1f", classData.classMark), 60))
            row.addView(createTableCell(classData.frequency.toString(), 50))
            row.addView(createTableCell(classData.cumFreqLess.toString(), 50))
            row.addView(createTableCell(classData.cumFreqGreater.toString(), 50))
            row.addView(createTableCell(String.format("%.1f", classData.relFreq), 60))

            resultsTable.addView(row)
        }
    }

    private fun createTableCell(text: String, minWidth: Int): TextView {
        return TextView(this).apply {
            this.text = text
            setPadding(16, 8, 16, 8)
            gravity = Gravity.CENTER
            setMinWidth(minWidth)
            textSize = 13f
        }
    }

    private fun showError(message: String) {
        errorText.text = message
        errorText.visibility = View.VISIBLE
        statsCard.visibility = View.GONE
        tableCard.visibility = View.GONE
    }

    private fun clearAll() {
        inputEditText.text.clear()
        errorText.visibility = View.GONE
        statsCard.visibility = View.GONE
        tableCard.visibility = View.GONE

        // Clear table rows except header
        val childCount = resultsTable.childCount
        if (childCount > 1) {
            resultsTable.removeViews(1, childCount - 1)
        }
    }

    data class ClassData(
        val classInterval: String,
        val classBoundaries: String,
        val classMark: Double,
        val frequency: Int,
        var cumFreqLess: Int = 0,
        var cumFreqGreater: Int = 0,
        var relFreq: Double = 0.0
    )
}