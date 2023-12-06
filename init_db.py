import sqlite3
import csv
from datetime import datetime

# Connect to SQLite database with a file path
conn = sqlite3.connect('weights.db')
cursor = conn.cursor()

# Create a table (using your provided CREATE TABLE statement)
cursor.execute('''
    CREATE TABLE AnimalWeights (
        AnimalWeightsSysID INT,
        Date DATETIME,
        EID BIGINT,
        Count INT,
        Mean FLOAT,
        Median FLOAT,
        MeanMedianDiff FLOAT,
        Range FLOAT,
        Skewness FLOAT,
        StandardError FLOAT,
        SERatio FLOAT,
        Kurtosis FLOAT,
        BiModalityCoefficient FLOAT,
        "Group" INT,
        subGroup INT,
        ScaleRange FLOAT,
        TotalScales INT,
        ScaleStat INT,
        ScaleWeight FLOAT,
        WeightVariance FLOAT,
        WeightedAverage FLOAT,
        CreatedAt VARCHAR(255),
        CreatedBy VARCHAR(255),
        UpdatedAt VARCHAR(255),
        UpdatedBy VARCHAR(255),
        EntitySysID INT,
        PanelSysID INT,
        ScaleSysID INT,
        CreatedByUserId INT,
        UpdatedByUserId INT
    );
''')

# Read and insert data from CSV
with open('DailyWeights.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header if present
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO AnimalWeights (
                AnimalWeightsSysID, Date, EID, Count, Mean, Median, MeanMedianDiff, Range,
                Skewness, StandardError, SERatio, Kurtosis, BiModalityCoefficient, "Group",
                subGroup, ScaleRange, TotalScales, ScaleStat, ScaleWeight, WeightVariance,
                WeightedAverage, CreatedAt, CreatedBy, UpdatedAt, UpdatedBy, EntitySysID,
                PanelSysID, ScaleSysID, CreatedByUserId, UpdatedByUserId
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', row)


# Commit changes and close connection
conn.commit()
conn.close()
