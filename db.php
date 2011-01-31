<?php
$dbhandle = sqlite_open('hack.db');
$query = sqlite_query($dbhandle, 'SELECT * FROM requests');
$result = sqlite_fetch_all($query, SQLITE_ASSOC);
foreach ($result as $entry) {
    print_r($entry);
}
?>

