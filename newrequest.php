<!DOCTYPE html>
<html lang="en" >

<head>
  <meta charset="UTF-8">
  <title>Sign-Up/Login Form</title>
  <link href='https://fonts.googleapis.com/css?family=Titillium+Web:400,300,600' rel='stylesheet' type='text/css'>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
  <link rel="stylesheet" href="css/style.css">

  <style>
  .form {
  background: rgba(15, 30, 34, 0.9);
  padding: 40px;
  max-width: 600px;
  margin: 60px 80px 120px 380px;
  border-radius: 4px;
  box-shadow: 0 4px 10px 4px rgba(19, 35, 47, 0.3);
}
  </style>

</head>

<body>
<?php
require("menu.php")
?>

  <div class="form animated fadeIn" >
      
      <ul class="tab-group">
        <li class="tab active"><a href="#signup">Summarised</a></li>
        <li class="tab"><a href="#login">Details</a></li>
      </ul>
      
      <div class="tab-content">
        <div id="signup">   
          <h1>Short Request Summary</h1>
          
          <form action="submitrequest.php" method="post">

          <div class="field-wrap">
            <label>
              Request Title<span class="req">*</span>
            </label>
            <input type="text"required autocomplete="off"/>
          </div>
          
          <div class="field-wrap">
            <label>
              Short Description<span class="req">*</span>
            </label>
            <input type="text"required autocomplete="off"/>
          </div>
          
          <input type="submit" class="button button-block"/>
          
          </form>

        </div>
        
        <div id="login">   
          <h1>Need to give more details?</h1>
          
          <form action="submitrequest.php" method="post">
          
            <div class="field-wrap">
            
            <textarea name="" id="" cols="30" rows="5"></textarea>
          </div>
          
          <input type="submit" class="button button-block"/>
          
          </form>

        </div>
        
      </div><!-- tab-content -->
      
</div> <!-- /form -->


  <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

  

    <script  src="js/index.js"></script>




</body>

</html>
