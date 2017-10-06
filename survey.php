<?php
    /*
     *početna stranica ankete, na kojoj se nalazi link ka opštim pitanjima i linkovi ka svakom predmetu
     */
    include_once "database.php";

    session_start();

    //pristup bez prethodnog logovanja
    if (!isset($_SESSION["id_studenta"])) {
        header("Location: index.php");
        die();
    }

    //logout korisnika
    if (isset($_GET["logout"]) && $_GET["logout"]==1) {
        session_destroy();
        header("Location: index.php");
        die();
    }
    //echo $_SESSION["id_semestra"];
?>

<!DOCTYPE html>
<html>
<head>
    <title>Anketa</title>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script>
        //        $(document).ready(function() {
        //            if ($("#greska").text() != "") {
        //                $("#greska").show(800);
        //            }
        //        });
    </script>
</head>
<body>
    <h1>Dobrodošli u raf anketu</h1>
    <br>
    <br>



            <form method="POST" action="questions.php">
                    <input type="hidden" value="fakultet" name="tip_pitanja" />
                    <input type="submit" class="btn btn-primary" value="Opšta pitanja vezana za nastavu na RAF-u">
            </form>
    <br>
        <div class="btn-group-vertical">
        <?php
            //dodavanje predmeta koje student slusa
            $query = "SELECT DISTINCT predmet.id_predmeta, predmet.naziv
                      FROM student_u_grupi
                      JOIN grupa ON student_u_grupi.id_grupe = grupa.id_grupe AND grupa.id_semestra = ?
                      JOIN drži_predmet ON student_u_grupi.id_grupe = drži_predmet.id_grupe AND student_u_grupi.id_studenta = ?
                      JOIN predmet ON drži_predmet.id_predmeta = predmet.id_predmeta";
            $stmt = $conn->prepare($query);
            $stmt->bind_param('ss', $_SESSION["id_semestra"], $_SESSION["id_studenta"]);
            $stmt->execute();
            $result = $stmt->get_result();
            while ($row = $result->fetch_assoc()) {
                ?>

                    <form method="POST" action="course.php">
                        <input type="hidden" value="<?php echo $row["id_predmeta"]; ?>" name="id_predmeta" />
                        <input type="hidden" value="<?php echo $row["naziv"]; ?>" name="naziv_predmeta" />

                            <input type="submit" class="btn btn-success" value="<?php echo $row["naziv"]; ?>">

                    </form>

                <?php
            }
        ?>
        </div>
    <br>
    <br>

    <a href="survey.php?logout=1" class="btn btn-danger" id="logout">Logout</a>

</body>
</html>