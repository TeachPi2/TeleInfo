


<?php
// Connexion, sélection de la base de données
$dbconn = mysql_connect("localhost","Pi", "juju")
    or die('Connexion impossible : ' . mysql_error());

mysql_select_db('EDF',$dbconn);


//Requête SQL pour compter le nombre d'enregistrement de IINST
$count_req="SELECT COUNT( * ) AS total FROM EDF WHERE etiquette LIKE 'IINST'";
// Exécution de la requête SQL
$req0 = mysql_query($count_req) or die('Erreur SQL !<br>'.$count_req.'<br>'.mysql_error());
//Récupération du résultat
$res=mysql_fetch_assoc($req0);
//Le résultat est en l'occurence un tableau qui contient une case 'total' on affiche donc le contenu de la case.
$count=(int)$res['total'];
//on calcule pour afficher les 30 derniers resultats
if( $count>30)
{
$limit=$count -30;
}

else
{
 $limit=0;
}

$sql = "SELECT data,ts FROM EDF WHERE etiquette LIKE 'IINST' LIMIT $limit,$count";
// on envoie la requête
$req = mysql_query($sql) or die('Erreur SQL !<br>'.$sql.'<br>'.mysql_error()); 

$TimeLineData=array();
// on fait une boucle qui va faire un tour pour chaque enregistrement
while($data = mysql_fetch_assoc($req))
    {
    // on stocke les informations dans un tableau
   
   $TimeLineData[]=array($data['ts'],(int)$data['data']);
    }

// on ferme la connexion à mysql
mysql_close();
// on encode en JSON pour google chart
$TimeLineData=json_encode($TimeLineData);


$HTML =<<<XYZ
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>Historique Conso EDF</title>
 <!-- Bootstrap core CSS -->
    <link href="bootstrap-3.3.4/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="starter-template.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
    <script src="bootstrap-3.3.4/docs/assets/js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
</head>

 <!--Load the AJAX API-->
  <script type="text/javascript" src="https://www.google.com/jsapi"></script>
  <script type="text/javascript">

    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});

    // Set a callback to run when the Google Visualization library is loaded.
    google.setOnLoadCallback(drawChart);

    // Callback that creates and populates a data table,
    // instantiates the pie chart, passes in the data and
    // draws it.
    function drawChart() {

    // Create our data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'ts');
    data.addColumn('number', 'IINST');
       data.addRows({$TimeLineData});

  // Set chart options
        var options = {title:'Historique Consommation EDF',
         titleTextStyle: {fontName: 'Lato', fontSize: 18, bold: true},
                       height: 400,
                       is3D: true,
         colors:['#0F4F8D','#2B85C1','#8DA9BF','#F2C38D','#E6AC03','#F09B35', '#D94308', '#013453'],
         chartArea:{left:30,top:30,width:'100%',height:'80%'},

vAxes:{
0:{title: 'Intensité (Amps)'}
}
};

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
    chart.draw(data, options);
  }
  // Make the charts responsive
      jQuery(document).ready(function(){
        jQuery(window).resize(function(){
          drawChart();
        });
      });
  </script>

<body>
 <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="teleinfo.html">TéléInfo</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="teleinfo.html">Home</a></li>
            <li class="active"><a href="#">Historique</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

<!--Div that will hold the pie chart-->
    <div id="chart_div"></div>

</body>
XYZ;
echo $HTML


?>


