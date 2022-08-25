var colorPicker;

function showModal() {
    $(".modal-window").show();
    colorPicker.color.hsl = { h: 0, s: 0, l: 100 };
}       

function hideModal() {
    $(".modal-window").hide();
    document.getElementById("textresult").style.color=colorPicker.color.rgbString;
}    


$(document).ready(function(){
    colorPicker = new iro.ColorPicker("#picker", {
        width: 200,
      });
});
function printText(){
    const text_input = document.getElementById("text_input").value;
    document.getElementById("textresult").innerText = text_input
}









