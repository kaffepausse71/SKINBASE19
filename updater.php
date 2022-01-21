<?php
	error_reporting(E_ALL);
	ini_set("display_errors",1);
	ini_set('max_execution_time',0);
	header('Content-Type:text/html;charset=utf-8');
	$handle = popen("python3 ".getcwd()."/updater.py","r");

	if (ob_get_level() == 0) 
		ob_start();

	while(!feof($handle)) {
		$buffer = fgets($handle);
		$buffer = trim(htmlspecialchars($buffer));
		echo "$buffer";
		echo str_pad("<br />",4096*16);
		ob_flush();
		flush();
    }

	pclose($handle);
	ob_end_flush();
?>