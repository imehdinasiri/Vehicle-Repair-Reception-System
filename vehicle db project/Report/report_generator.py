import db_config
import pyodbc

def fetch_data(query, params):
    conn = db_config.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor, conn
    except Exception as e:
        cursor.close()
        conn.close()
        raise RuntimeError(f"Database query failed: {e}")

def get_income_by_services_and_parts(start_date, end_date):
    query = """
    SELECT 
        SUM(ISNULL(s.Cost, 0) + ISNULL(g.UnitPrice * pu.QuantityUsed, 0)) AS TotalIncome
    FROM RepairOrder ro
    LEFT JOIN RepairOrderService ros ON ro.RepairOrderID = ros.RepairOrderID
    LEFT JOIN Service s ON ros.ServiceID = s.ServiceID
    LEFT JOIN Part_Used pu ON ro.RepairOrderID = pu.RepairOrderID
    LEFT JOIN Goods g ON pu.GoodsID = g.GoodsID
    WHERE ro.OrderDate BETWEEN ? AND ?
    """
    try:
        cursor, conn = fetch_data(query, (start_date, end_date))
        with cursor, conn:
            row = cursor.fetchone()
            if row and row.TotalIncome is not None:
                return [{"TotalIncome": row.TotalIncome}]
            else:
                return [{"message": "No income data found for this date range."}]
    except Exception as e:
        return [{"error": str(e)}]

def get_acceptance_count(start_date, end_date):
    query = """
    SELECT 
        CONVERT(DATE, r.ReceptionDate) AS ReportDate, 
        COUNT(*) AS NumberOfReceptions
    FROM Reception r
    WHERE r.ReceptionDate BETWEEN ? AND ?
    GROUP BY CONVERT(DATE, r.ReceptionDate)
    ORDER BY ReportDate
    """
    try:
        cursor, conn = fetch_data(query, (start_date, end_date))
        with cursor, conn:
            results = [
                {"Date": row.ReportDate, "NumberOfReceptions": row.NumberOfReceptions}
                for row in cursor
            ]
        return results if results else [{"message": "No reception data found for this date range."}]
    except Exception as e:
        return [{"error": str(e)}]

def get_repairs_by_type_and_income(start_date, end_date):
    query = """
    SELECT 
        s.ServiceName, COUNT(ros.RepairOrderID) AS RepairCount,
        SUM(ISNULL(s.Cost, 0)) AS TotalIncome
    FROM RepairOrder ro
    LEFT JOIN RepairOrderService ros ON ro.RepairOrderID = ros.RepairOrderID
    LEFT JOIN Service s ON ros.ServiceID = s.ServiceID
    WHERE ro.OrderDate BETWEEN ? AND ?
    GROUP BY s.ServiceName
    ORDER BY TotalIncome DESC
    """
    try:
        cursor, conn = fetch_data(query, (start_date, end_date))
        with cursor, conn:
            results = [
                {"ServiceType": row.ServiceName, "Repairs": row.RepairCount, "Income": row.TotalIncome}
                for row in cursor
            ]
            if not results:
                print("Debug: No rows fetched from query. Check OrderDate or RepairOrderService data.")
            return results if results else [{"message": "No repair data found for this date range."}]
    except Exception as e:
        return [{"error": str(e)}]

def get_repair_costs_by_plate(start_date, end_date):
    query = """
    SELECT 
        c.LicensePlate, 
        COUNT(DISTINCT ro.RepairOrderID) AS NumberOfRepairs,
        SUM(ISNULL(s.Cost, 0)) AS ServiceCost,
        SUM(ISNULL(g.UnitPrice * pu.QuantityUsed, 0)) AS PartsCost,
        SUM(ISNULL(s.Cost, 0) + ISNULL(g.UnitPrice * pu.QuantityUsed, 0)) AS TotalCost
    FROM Car c
    JOIN Reception r ON c.CarID = r.CarID
    JOIN RepairOrder ro ON r.ReceptionID = ro.ReceptionID
    LEFT JOIN RepairOrderService ros ON ro.RepairOrderID = ros.RepairOrderID
    LEFT JOIN Service s ON ros.ServiceID = s.ServiceID
    LEFT JOIN Part_Used pu ON ro.RepairOrderID = pu.RepairOrderID
    LEFT JOIN Goods g ON pu.GoodsID = g.GoodsID
    WHERE ro.OrderDate BETWEEN ? AND ?
    GROUP BY c.LicensePlate
    ORDER BY TotalCost DESC
    """
    try:
        cursor, conn = fetch_data(query, (start_date, end_date))
        with cursor, conn:
            results = [
                {
                    "Plate": row.LicensePlate,
                    "NumberOfRepairs": row.NumberOfRepairs,
                    "ServiceCost": row.ServiceCost,
                    "PartsCost": row.PartsCost,
                    "TotalCost": row.TotalCost
                }
                for row in cursor
            ]
        return results if results else [{"message": "No cost data found for this date range."}]
    except Exception as e:
        return [{"error": str(e)}]

def get_top_customers(start_date, end_date):
    query = """
    SELECT TOP 20
        cu.FullName,
        cu.Mobile AS PhoneNumber,
        COUNT(DISTINCT r.ReceptionID) AS VisitCount,
        MAX(r.ReceptionDate) AS LastVisit
    FROM Customer cu
    JOIN Car c ON cu.CustomerID = c.CustomerID
    JOIN Reception r ON c.CarID = r.CarID
    WHERE r.ReceptionDate BETWEEN ? AND ?
    GROUP BY cu.FullName, cu.Mobile
    ORDER BY VisitCount DESC
    """
    try:
        cursor, conn = fetch_data(query, (start_date, end_date))
        with cursor, conn:
            results = [
                {
                    "FullName": row.FullName,
                    "PhoneNumber": row.PhoneNumber,
                    "VisitCount": row.VisitCount,
                    "LastVisit": row.LastVisit
                }
                for row in cursor
            ]
        return results if results else [{"message": "No frequent customers found for this date range."}]
    except Exception as e:
        return [{"error": str(e)}]