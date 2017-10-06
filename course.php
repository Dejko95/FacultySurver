<?php
    /*
     * na ovoj stranici nalaze se sekcije pitanja za odabrani predmet. Generalna pitanja, i za svakog nastavnika posebno.
     */
    include_once "database.php";

    session_start();

    if (!(isset($_SESSION["id_studenta"]) && $_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["id_predmeta"]) && isset($_POST["naziv_predmeta"]))) {
        header("Location: survey.php");
        die();
    }

?>

<!DOCTYPE html>
<html>
<head>
    <title>Kurs</title>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script>
    </script>
</head>
<body>
    <h1><?php echo $_POST["naziv_predmeta"]; ?></h1>

    <table>
        <tr>
            <form method="POST" action="questions.php">
                <td>
                    <input type="hidden" value="predmet" name="tip_pitanja" />
                    <input type="hidden" value="<?php echo $_POST["id_predmeta"]; ?>" name="id_predmeta" />
                    <input type="hidden" value="<?php echo $_POST["naziv_predmeta"]; ?>" name="naziv_predmeta" />
                    <input type="submit" class="btn btn-info" value="Oceni predmet">
                </td>
            </form>
        </tr>
        <br>
        <?php
        //listanje svih nastavnika na izabranom predmetu
        $query = "SELECT nastavnik.ime, nastavnik.prezime, nastavnik.tip, drži_predmet.id
                  FROM student_u_grupi 
                  JOIN drži_predmet ON student_u_grupi.id_grupe = drži_predmet.id_grupe AND student_u_grupi.id_studenta = ? AND drži_predmet.id_predmeta = ?
                  JOIN nastavnik ON drži_predmet.id_nastavnika = nastavnik.id_nastavnika";
        $stmt = $conn->prepare($query);
        $stmt->bind_param('ss', $_SESSION["id_studenta"], $_POST["id_predmeta"]);
        $stmt->execute();
        $result = $stmt->get_result();
        while ($row = $result->fetch_assoc()) {
            ?>
            <tr>
                <form method="POST" action="questions.php">
                    <td>
                        <input type="hidden" value="nastavnik" name="tip_pitanja" />
                        <input type="hidden" value="<?php echo $row["id"]; ?>" name="id_drži_predmet" />
                        <input type="hidden" value="<?php echo $row["ime"]." ".$row["prezime"]; ?>" name="nastavnik" />
                        <input type="hidden" value="<?php echo $_POST["id_predmeta"]; ?>" name="id_predmeta" />
                        <input type="hidden" value="<?php echo $_POST["naziv_predmeta"]; ?>" name="naziv_predmeta" />
                        <input type="submit" class="btn btn-warning" value="<?php echo $row["ime"]." ".$row["prezime"]." - ".$row["tip"]; ?>">
                    </td>
                </form>
            </tr>
            <?php
        }
        ?>
    </table>
    <br>

    <form method="GET" action="survey.php">
        <input type="submit" class="btn btn-basic" value="Vrati se na početak">
    </form>

</body>
</html>
