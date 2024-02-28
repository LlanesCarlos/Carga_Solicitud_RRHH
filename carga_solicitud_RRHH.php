<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carga de Solicitud</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
        }
        form {
            margin-top: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"],
        input[type="date"],
        input[type="time"] {
            width: calc(100% - 12px);
            padding: 6px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Carga de Solicitud</h1>
        <form method="POST" action="carga_solicitud_RRHH.php">
            <label for="cedula">Documento</label>
            <input type="text" name="cedula" id="cedula" placeholder="Ingrese número de cédula." required>
            <label for="fecha_desde">¿Desde qué día?</label>
            <input type="date" name="fecha_desde" id="fecha_desde" required>
            <label for="desde_hora">¿Desde qué hora?</label>
            <input type="time" name="desde_hora" id="desde_hora" required>
            <label for="fecha_hasta">¿Hasta qué día?</label>
            <input type="date" name="fecha_hasta" id="fecha_hasta" required>
            <label for="hasta_hora">¿Hasta qué hora?</label>
            <input type="time" name="hasta_hora" id="hasta_hora" required>
            <label for="fundamento">Fundamento</label>
            <input type="text" name="fundamento" id="fundamento" placeholder="Motivo por el cual se hace la solicitud. Ej: Permiso para viaje." required>
            <label for="encargado">Reemplazo</label>
            <input type="text" name="encargado" id="encargado" placeholder="En caso de ser necesario, ¿quién reemplaza al solicitante durante su ausencia?" required>
            <input type="submit" value="Generar">
        </form>
    </div>
    <script>
        // Get today's date in the format yyyy-mm-dd
        var today = new Date().toISOString().split('T')[0];
        
        // Set the default value of the fecha_desde input field to today's date
        document.getElementById("fecha_desde").value = today;
    </script>
</body>
</html>

<?php
if (php_sapi_name() == 'cli') {
    // Handle command line execution
    // Assuming command line arguments are provided as $argv
    // Example: php script.php arg1 arg2 ...
    $cedula = isset($argv[1]) ? $argv[1] : "";
    $fecha_desde = isset($argv[2]) ? $argv[2] : "";
    $fecha_hasta = isset($argv[3]) ? $argv[3] : "";
    $hora_desde = isset($argv[4]) ? $argv[4] : "";
    $hora_hasta = isset($argv[5]) ? $argv[5] : "";
    $fundamento = isset($argv[6]) ? implode(" ", array_slice($argv, 6)) : "";
    $encargado = isset($argv[7]) ? $argv[7] : "";

    // Log file path
    $myfile = fopen("/path/to/log.txt", "w") or die("Unable to open file!");
    $log = "$cedula $fecha_desde $fecha_hasta $hora_desde $hora_hasta $fundamento";
    fwrite($myfile, $log);
    fclose($myfile);
} else {
    // Handle web server execution
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $cedula = isset($_POST['cedula']) ? $_POST['cedula'] : "";
        $fecha_desde = isset($_POST['fecha_desde']) ? $_POST['fecha_desde'] : "";
        $fecha_hasta = isset($_POST['fecha_hasta']) ? $_POST['fecha_hasta'] : "";
        $hora_desde = isset($_POST['desde_hora']) ? $_POST['desde_hora'] : "";
        $hora_hasta = isset($_POST['hasta_hora']) ? $_POST['hasta_hora'] : "";
        $fundamento = isset($_POST['fundamento']) ? $_POST['fundamento'] : "";
        $encargado = isset($_POST['encargado']) ? $_POST['encargado'] : "";
        // Log file path
        $myfile = fopen("/path/to/log.txt", "w") or die("Unable to open file!");
        $log = "$cedula $fecha_desde $fecha_hasta $hora_desde $hora_hasta $fundamento | $encargado";
        fwrite($myfile, $log);
        fclose($myfile);
        // Execute Python script
        exec("python3 /path/to/pdf.py");
        // Wait for 5 seconds (adjust as needed)
        sleep(5);

        // Redirect to the corresponding destination PDF
        header("Location: path/to/solicitud_$cedula.pdf");
        exit; // Make sure that subsequent code is not executed after redirection
    }
}
?>
