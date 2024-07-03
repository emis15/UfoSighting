from database.DB_connect import DBConnect
from model.stato import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT YEAR(datetime) as year 
                    FROM sighting s
                    WHERE YEAR(datetime) >= 1910 AND YEAR(datetime) <= 2014
                    ORDER BY year DESC"""

        cursor.execute(query, )

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getShapesfromYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT shape 
                    FROM sighting s 
                    WHERE YEAR(datetime) = %s
                    AND shape IS NOT NULL 
                    AND shape != ''
                    ORDER BY shape ASC"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getWeight(year, shape, edge):
        s1 = edge[0].id
        s2 = edge[1].id
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT COUNT(*) as weight
                    FROM sighting s
                    where  year(s.datetime) = %s and s.shape = %s
                    and (upper(s.state) = %s or upper(s.state) = %s)"""

        cursor.execute(query, (year, shape, s1, s2))

        for row in cursor:
            result = row['weight']

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllWeightedNeigh(year, shape, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1, n.state2 , count(*) as N
                        FROM sighting s , neighbor n 
                        where year(s.`datetime`) = %s
                        and s.shape = %s
                        and (s.state = n.state1 or s.state = n.state2 )
                        and n.state1 < n.state2
                        group by n.state1 , n.state2 """

        cursor.execute(query, (year, shape))

        for row in cursor:
            result.append((idMap[row['state1']], idMap[row['state2']], row["N"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * from state s """

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select state1 as s1, state2 as s2
                    from neighbor n 
                    where n.state1 > n.state2 """

        cursor.execute(query)

        for row in cursor:
            result.append((idMap[row['s1']], idMap[row['s2']]))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select state1 as s1, state2 as s2
                    from neighbor n 
                    where n.state1 > n.state2 """

        cursor.execute(query)

        for row in cursor:
            result.append((idMap[row['s1']], idMap[row['s2']]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllPesiTemaPassato(year, giorni, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.state1 as state1, t.state2 as state2, COUNT(*) as peso
                    FROM (
                        SELECT n.state1, n.state2, ABS(DATEDIFF(s.datetime, s2.datetime)) as diff
                        FROM neighbor n, 
                             (SELECT s1.state, s1.datetime 
                              FROM sighting s1 
                              WHERE YEAR(s1.datetime) = %s) s, 
                             (SELECT s1.state, s1.datetime 
                              FROM sighting s1 
                              WHERE YEAR(s1.datetime) = %s) s2
                        WHERE s.state = n.state1 
                          AND s2.state = n.state2 
                          AND n.state1 < n.state2
                    ) as t
                    WHERE t.diff <= %s
                    GROUP BY t.state1, t.state2 """

        cursor.execute(query, (year, year, giorni))

        for row in cursor:
            result.append((idMap[row['state1']], idMap[row['state2']], row["peso"]))

        cursor.close()
        conn.close()
        return result