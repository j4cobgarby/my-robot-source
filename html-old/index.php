<?php
$allowed = array("left_forwards", "left_backwards", "left_stop", "right_forwards", "right_backwards", "right_stop", "all_forwards", "all_backwards",
	"all_stop", "test_motor", "test_network", "shutdown_pi", "reboot_pi");
if (isset($_POST["cmd"]) && in_array($_POST["cmd"], $allowed)) {
	echo $_POST["cmd"];
	echo shell_exec("sudo /usr/bin/python3 /home/pi/code/robot/cmds/".$_POST["cmd"].".py");
}
?>
<html>
	<head>
		<title>Ctrl Panel</title>
	</head>
	<body>
		<h1>Robot control panel</h1>
		<form action="" method="post">
			<hr>Left wheel<br>
			<input type="submit" name="cmd" value="left_forwards">
			<input type="submit" name="cmd" value="left_backwards">
			<input type="submit" name="cmd" value="left_stop">
			<hr>Right wheel<br>
			<input type="submit" name="cmd" value="right_forwards">
			<input type="submit" name="cmd" value="right_backwards">
			<input type="submit" name="cmd" value="right_stop">
			<hr>Master<br>
			<input type="submit" name="cmd" value="all_forwards">
			<input type="submit" name="cmd" value="all_backwards">
			<input type="submit" name="cmd" value="all_stop">
			<hr>Test<br>
			<input type="submit" name="cmd" value="test_motor">
			<input type="submit" name="cmd" value="test_network">
			<hr>Power<br>
			<input type="submit" name="cmd" value="all_stop">
			<input type="submit" name="cmd" value="shutdown_pi" style="color:red;font-weight:bold;">
			<input type="submit" name="cmd" value="reboot_pi" style="color:orange;font-weight:bold;">
		</form>
	</body>
</html>
