<!DOCTYPE html>
<html lang="en" >

<head>
  <meta charset="UTF-8">
  <title>Sign-Up/Login Form</title>
  <link href='https://fonts.googleapis.com/css?family=Titillium+Web:400,300,600' rel='stylesheet' type='text/css'>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="css/style.css">

  <style>
.tab-group li a {
  width: 25%; 
}
  </style>

</head>

<body>
<?php
require("menu-admin.php")
?>
<?php
require("sidebar.php")
?>

<div class="main">
  <div id="content">
    <div id="left">
    <div class="entry">
    <h2><a href="#">Request Title:Request Short Description</a></h2>
    <p>This will contain the extensive details of any given request in case the user decided to supply any at
    the point of creating a new request. The next words are just to fill the space just to show what a detailed request 
    would look like.</p>
    <form action="updaterequest.php" method="post">
    <div class="field-wrap">
          <input type="text" id="commentbox" style="display:none" autocomplete="off" />
        </div>
    <ul class="tab-group">
        <li class="tab active"><a onclick="displayCommentBox()">Add Comment</a></li>
        <li class="tab"><input type="submit" name="resolve" class="approve" value="Resolve"/></li>
        <li class="tab"><input type="submit" name="reject"  class="approve" value="Reject"/></li>
      </ul> 
      
      </form>
      <p class="meta"><span class="date">May 22,2018</span> Posted by Rutale | Status: Pending, Administrator Comment | No comments</p>
  </div>

      <div class="entry">
        <h2><a href="#">Request Title:Request Short Description</a></h2>
        <p>This will contain the extensive details of any given request in case the user decided to supply any at
        the point of creating a new request. The next words are just to fill the space just to show what a detailed request 
        would look like.</p>
        <form action="updaterequest.php" method="post">
        <div class="field-wrap">
              <input type="text" id="commentbox" style="display:none" autocomplete="off" />
            </div>
        <ul class="tab-group">
            <li class="tab active"><a onclick="displayCommentBox()">Add Comment</a></li>
            <li class="tab"><input type="submit" name="resolve" class="approve" value="Resolve"/></li>
            <li class="tab"><input type="submit" name="reject"  class="approve" value="Reject"/></li>
          </ul> 
          
          </form>
          <p class="meta"><span class="date">May 22,2018</span> Posted by Rutale | Status: Pending, Administrator Comment | No comments</p>
      </div>

      <div class="entry">
      <h2><a href="#">Request Title:Request Short Description</a></h2>
      <p>This will contain the extensive details of any given request in case the user decided to supply any at
      the point of creating a new request. The next words are just to fill the space just to show what a detailed request 
      would look like.</p>
      <form action="updaterequest.php" method="post">
      <div class="field-wrap">
            <input type="text" id="commentbox" style="display:none" autocomplete="off" />
          </div>
      <ul class="tab-group">
          <li class="tab active"><a onclick="displayCommentBox()">Add Comment</a></li>
          <li class="tab"><input type="submit" name="resolve" class="approve" value="Resolve"/></li>
          <li class="tab"><input type="submit" name="reject"  class="approve" value="Reject"/></li>
        </ul> 
        
        </form>
        <p class="meta"><span class="date">May 22,2018</span> Posted by Rutale | Status: Pending, Administrator Comment | No comments</p>
    </div>

</div>

  <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
  <script  src="js/index.js"></script>
  <script src="js/dynamicstyle.js"></script>



</body>

</html>
