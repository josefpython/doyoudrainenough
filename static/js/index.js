console.log("javascript正在运行");
var widthHigher = null;


function responsive() {

   if(window.innerWidth <= window.innerHeight) {
        resp(type="toMob");
        widthHigher = false;
   } else { widthHigher = true; }

   setInterval(function() {
      if(window.innerHeight < window.innerWidth && widthHigher == false) {

         resp(type="toPC");
         widthHigher = true;
      } else if(window.innerHeight > window.innerWidth && widthHigher == true) {

         resp(type="toMob");
         widthHigher = false;
      }
   }, 1000)
}


function blink() {

    console.log("页面内容加载");
    var f = document.getElementById('text1');
    setInterval(function() {
       f.style.color = (f.style.color == 'yellow' ? 'red' : 'yellow');
    }, 500);

    var x = document.getElementById('pornad');
    setInterval(function() {
       x.style.borderColor = (x.style.borderColor == 'white' ? 'red' : 'white');
    }, 200);
 }

function blockPopup() {
   u = document.getElementById("text3");
   u.style.visibility = "hidden"
   console.log("弹出窗口已隐藏");
   setTimeout(function() {
      u.style.visibility = "visible"
      console.log("弹出负载");
   }, 2500);
}

function resp(type) {

   var stylesheet = null;

   if(type=="toMob"){
      stylesheet = "/static/styles/m_index.css"
      console.log("CSS更改为移动");

   }else if(type=="toPC"){
      stylesheet = "/static/styles/index.css"
      console.log("CSS更改为PC");
   }

   document.getElementById("stylesheet").href=stylesheet;

}