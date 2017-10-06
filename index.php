<?php
    require_once "database.php";

    session_start();

    if ($_SERVER["REQUEST_METHOD"] == "GET") {
        //echo "get";
        if (isset($_SESSION["id_studenta"])) {
            header("Location: survey.php");
            die();
        }
    } else {
        //echo "post";
        if (isset($_POST["username"]) && isset($_POST["password"])) {
            $username = $_POST["username"];
            $password = $_POST["password"];

            $query = "SELECT * FROM studentski_nalog where username=? AND password=?";
            $stmt = $conn->prepare($query);
            $stmt->bind_param('ss', $username, $password);
            $stmt->execute();
            $result = $stmt->get_result();
            if ($row = $result->fetch_assoc()) {
                $_SESSION["id_studenta"] = $row["id_studenta"];
                //odmah nalazimo i odgovarajuci semestar
                $query = "SELECT * FROM trenutni_semestar";
                $result = $conn->query($query);
                if ($row = $result->fetch_assoc()) {
                    $_SESSION["školska_godina"] = $row["školska_godina"];
                    $_SESSION["tip_semestra"] = $row["tip_semestra"];
                }
                //nalazimo indeks semestra kome pripada ulogovani korisnik
                $query = "SELECT semestar.id_semestra FROM student_u_grupi 
                          JOIN grupa ON grupa.id_grupe = student_u_grupi.id_grupe AND student_u_grupi.id_studenta = ?
                          JOIN semestar ON grupa.id_semestra = semestar.id_semestra 
                          AND semestar.školska_godina = ? AND semestar.tip_semestra = ?";
                $stmt = $conn->prepare($query);
                $stmt->bind_param('sss', $_SESSION["id_studenta"], $_SESSION["školska_godina"], $_SESSION["tip_semestra"]);
                $stmt->execute();
                $result = $stmt->get_result();
                if ($row = $result->fetch_assoc()) {
                    $_SESSION["id_semestra"] = $row["id_semestra"];
                }

                header("Location: survey.php");
                die();
            } else {
                $greska = "wrong username or password";
            }
        }
    }
?>

<!DOCTYPE html>
<html>
<head>
    <title>Anketa - logovanje</title>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script>
        $(document).ready(function() {
            if ($("#greska").text() != "") {
                $("#greska").show(800);
            }
        });
    </script>
</head>
<body>
    <h1>Prijava:</h1>
    <br>
    <div id="greska" style="display:none; color:red; font-weight:bold;"><?php if (isset($greska)) echo $greska; ?></div>
    <br>
    <form class="form-horizontal" action="" method="post">
        <div class="form-group">
            <label class="control-label col-sm-2" for="email">Korisničko ime:</label>
            <div class="col-sm-10">
                <input type="text" class="form-control" name="username" id="username" value="" placeholder="Unesite korisničko ime"></input>
            </div>
        </div>
        <div class="form-group">
            <label class="control-label col-sm-2" for="pwd">Lozinka:</label>
            <div class="col-sm-10">
                <input type="password" class="form-control" name="password" id="password" placeholder="Unesite lozinku"></input>
            </div>
        </div>
        <div class="form-group">
            <div class="col-sm-offset-2 col-sm-10">
                <input type="submit" id="submit" class="btn btn-primary" value="Prijavi se"></input>
            </div>
        </div>
    </form>



</body>
</html>
