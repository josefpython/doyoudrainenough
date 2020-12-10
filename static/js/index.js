console.log("javascript正在运行");

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