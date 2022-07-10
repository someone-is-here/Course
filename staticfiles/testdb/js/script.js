const canvas = window.canvas1;
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let particlesArray = undefined;

let mouse = {
  x: null,
  y: null,
  radius: (canvas.height/80)*(canvas.width/80)
};
window.addEventListener('mousemove',function(event){
  mouse.x = event.x;
  mouse.y = event.y;
});

class Particle{
  constructor(x,y,directionX,directionY,size,color){
    this.x = x;
    this.y = y;
    this.directionX = directionX;
    this.directionY = directionY;
    this.size = size;
    this.color = color;
  }
  draw(){
    ctx.beginPath();
    ctx.arc(this.x,this.y,this.size, 0,Math.PI * 2,false);
    ctx.fillStyle = 'rgba(93, 211, 77, 0.932)';
    ctx.fill();
  }
  update(){
    if(this.x > canvas.width || this.x < 0){
      this.directionX = -this.directionX;
    }
    if(this.y > canvas.height || this.y < 0){
      this.directionY = -this.directionY;
    }
    let dx = mouse.x - this.x;
    let dy = mouse.y - this.y;
    let distance = Math.sqrt(dx*dx + dy*dy);

    if(distance < mouse.radius + this.size){
        if(mouse.x < this.x && this.x < canvas.width - this.size * 10){
          this.x += 10;
        }
        if(mouse.x > this.x && this.x > this.size * 10){
          this.x -= 10;
        }
        if(mouse.y < this.y && this.y < canvas.height - this.size * 10){
          this.y += 10;
        }
        if(mouse.y > this.y && this.y > this.size * 10){
          this.y -= 10;
        }
    }
    this.x += this.directionX;
    this.y += this.directionY;
    this.draw();
  }
}
function init(){
  particlesArray = [];
  let numberOfParticles = (canvas.height * canvas.width) / 9000;
  for( i = 0; i < numberOfParticles*2; i++){
    size = (Math.random() * 5) + 1;
    x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
    y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
    directionX = (Math.random() * 5) - 2.5;
    directionY = (Math.random() * 5) - 2.5;
    color = 'rgba(93, 211, 77, 0.932)';
    particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
  }
}
function animate(){
  requestAnimationFrame(animate);
  ctx.clearRect(0, 0, innerWidth, innerHeight);
  for(i = 0; i < particlesArray.length; i++){
    particlesArray[i].update();
  }
  connect();
}

function connect(){
  let opacityValue = 1;
  for(i=0;i<particlesArray.length;i++){
    for(j=0;j<particlesArray.length;j++){
      distance=Math.pow(particlesArray[i].x-particlesArray[j].x,2)+Math.pow(particlesArray[i].y-particlesArray[j].y,2);
      if(distance < (canvas.width*canvas.height)/49){
        opacityValue = 1 - (distance/20000);
        ctx.strokeStyle = 'rgb(93, 211, 77,'+ opacityValue +')';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(particlesArray[i].x,particlesArray[i].y);
        ctx.lineTo(particlesArray[j].x,particlesArray[j].y);
        ctx.stroke();
      }
    }
  }
}

init();
animate();

window.addEventListener('resize',function(){
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  mouse.radius=(canvas.height/80)*(canvas.width/80);
  init();
});