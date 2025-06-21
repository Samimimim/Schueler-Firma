const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");
canvas.width = 400;
canvas.height = 400;
document.body.appendChild(canvas);

let player = { x: 200, y: 350, w: 40, h: 40, color: "blue" };
let enemy = {
  x: Math.random() * 360,
  y: 0,
  w: 40,
  h: 40,
  color: "red",
  speed: 2,
};
let score = 0;
let gameOver = false;

function drawRect(obj) {
  ctx.fillStyle = obj.color;
  ctx.fillRect(obj.x, obj.y, obj.w, obj.h);
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawRect(player);
  drawRect(enemy);
  ctx.fillStyle = "black";
  ctx.fillText("Score: " + score, 10, 20);
  if (gameOver) {
    ctx.font = "30px Arial";
    ctx.fillText("Game Over!", 120, 200);
  }
}

function update() {
  if (gameOver) return;
  enemy.y += enemy.speed;
  if (enemy.y > canvas.height) {
    enemy.y = 0;
    enemy.x = Math.random() * (canvas.width - enemy.w);
    score++;
    enemy.speed += 0.2;
  }
  // Collision detection
  if (
    player.x < enemy.x + enemy.w &&
    player.x + player.w > enemy.x &&
    player.y < enemy.y + enemy.h &&
    player.y + player.h > enemy.y
  ) {
    gameOver = true;
  }
}

function loop() {
  update();
  draw();
  if (!gameOver) requestAnimationFrame(loop);
}

document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowLeft" && player.x > 0) player.x -= 20;
  if (e.key === "ArrowRight" && player.x < canvas.width - player.w)
    player.x += 20;
  if (gameOver && e.key === "r") location.reload();
});

loop();
