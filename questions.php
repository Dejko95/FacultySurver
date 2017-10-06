<?php
    /*
     * na ovoj stranici nalaze nalaze se odgovarajuca pitanja
     */

    include_once "database.php";

    session_start();

    if (!(isset($_SESSION["id_studenta"]) && $_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["tip_pitanja"]))) {
        header("Location: survey.php");
        die();
    }

    if ($_POST["tip_pitanja"] == "fakultet") {
        $subject = "nastavi na RAF-u";
    } else if ($_POST["tip_pitanja"] == "predmet") {
        $subject = "predmetu " . $_POST["naziv_predmeta"];
        //echo $_POST["id_predmeta"] . " " . $_POST["naziv_predmeta"];
    } else {
        $subject = "nastavniku " . $_POST["nastavnik"] . " na predmetu " . $_POST["naziv_predmeta"];
        //echo $_POST["id_predmeta"] . " " . $_POST["naziv_predmeta"];
    }

?>

<!DOCTYPE html>
<html>
<head>
    <title>Pitanja</title>
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
    <h1>Pitanja o <?php echo $subject ?></h1>
    <form method="POST" action="finish.php" id="questions_form">
        <input type="hidden" value="<?php echo $_POST["tip_pitanja"]; ?>" name="tip_pitanja" />
        <?php if (isset($_POST["id_drži_predmet"]))  { ?>
            <input type="hidden" value="<?php echo $_POST["id_drži_predmet"]; ?>" name="id_drži_predmet" />
        <?php } ?>
        <?php if (isset($_POST["id_predmeta"])) { ?>
            <input type="hidden" value="<?php echo $_POST["id_predmeta"]; ?>" name="id_predmeta" />
        <?php } ?>
        <?php if (isset($_POST["naziv_predmeta"])) { ?>
            <input type="hidden" value="<?php echo $_POST["naziv_predmeta"]; ?>" name="naziv_predmeta" />
        <?php } ?>
        <?php
            $query = "SELECT * FROM pitanje WHERE tip = ?";
            $stmt = $conn->prepare($query);
            $stmt->bind_param('s', $_POST["tip_pitanja"]);
            $stmt->execute();
            $result = $stmt->get_result();
            while ($row = $result->fetch_assoc()) {
                ?>
                <p><?php echo $row["tekst"]; ?></p>
                <?php
                    //ako je vec odgovoreno, ucitamo taj odgovor
                    if ($_POST["tip_pitanja"] == "fakultet") {
                        $query = "SELECT odgovor FROM odgovor_fakultet WHERE id_pitanja = ? AND id_studenta = ? AND id_semestra = ?";
                        $stmt = $conn->prepare($query);
                        $stmt->bind_param('sss', $row["id_pitanja"], $_SESSION["id_studenta"], $_SESSION["id_semestra"]);
                    } else if ($_POST["tip_pitanja"] == "predmet") {
                        $query = "SELECT odgovor FROM odgovor_predmet WHERE id_pitanja = ? AND id_studenta = ? AND id_predmeta = ? AND id_semestra = ?";
                        $stmt = $conn->prepare($query);
                        $stmt->bind_param('ssss', $row["id_pitanja"], $_SESSION["id_studenta"], $_POST["id_predmeta"], $_SESSION["id_semestra"]);
                    } else {
                        $query = "SELECT odgovor FROM odgovor_nastavnik WHERE id_pitanja = ? AND id_studenta = ? AND id_drži_predmet = ? AND id_semestra = ?";
                        $stmt = $conn->prepare($query);
                        $stmt->bind_param('ssss', $row["id_pitanja"], $_SESSION["id_studenta"], $_POST["id_drži_predmet"], $_SESSION["id_semestra"]);
                    }
                    $stmt->execute();
                    $result_answer = $stmt->get_result();
                    if ($row_answer = $result_answer->fetch_assoc()) {
                        $answer = $row_answer["odgovor"];
                    }
                    if (trim($row["format"]) == "ocena") {
                        ?>
                        <input type="radio" name="<?php echo $row["id_pitanja"]; ?>" value="1" <?php if (isset($answer) && $answer == "1") echo "checked"; ?>> 1
                        <input type="radio" name="<?php echo $row["id_pitanja"]; ?>" value="2" <?php if (isset($answer) && $answer == "2") echo "checked"; ?>> 2
                        <input type="radio" name="<?php echo $row["id_pitanja"]; ?>" value="3" <?php if (isset($answer) && $answer == "3") echo "checked"; ?>> 3
                        <input type="radio" name="<?php echo $row["id_pitanja"]; ?>" value="4" <?php if (isset($answer) && $answer == "4") echo "checked"; ?>> 4
                        <input type="radio" name="<?php echo $row["id_pitanja"]; ?>" value="5" <?php if (isset($answer) && $answer == "5") echo "checked"; ?>> 5
                        <?php
                    } else {
                        ?>
                        <textarea rows="4" cols="50" form="questions_form" name="<?php echo $row["id_pitanja"]; ?>" placeholder="Unesite vaš odgovor..."><?php if (isset($answer)) echo $answer; ?></textarea>
                        <?php
                    }
                ?>
                <hr>
                <?php
            }
        ?>
        <input type="submit" value="Sačuvaj" class="btn btn-success">
    </form>

    <form method="GET" action="survey.php">
        <input type="submit" value="Odustani" class="btn btn-danger">
    </form>

</body>
</html>
