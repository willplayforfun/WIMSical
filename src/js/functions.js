function getHTTP(){
if (window.XMLHttpRequest) return new XMLHttpRequest();
else return new ActiveXObject("Microsoft.XMLHTTP");
 }
 
 function updateContent(i){
 var xmlhttp = getHTTP();
xmlhttp.open("GET",i,false);
xmlhttp.send();

  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
		
 document.getElementById('content').innerHTML  =xmlhttp.responseText;
	}
 }
 function updateBar(i){
	 updateContent(i); 
	 fin = i;
	 if(fin.length>='&ajax=1'.length){
		fin = fin.substring(0, fin.length-'&ajax=1'.length);
	 }
	 window.history.pushState('hack-tj.appspot.com/'+fin,'','/'+fin)
	 $('#navigation > li.active').removeClass();
	 $('#'+i+'')[0].className= 'active';
 }