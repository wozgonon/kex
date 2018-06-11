const scale_x = 1/64
const scale_y = 200

function setTransform (ctx, x0, y0) {
//    let angle_sine = Math.sin(Math.PI)
//    let angle_cosine = Math.cos(Math.PI)
//    ctx.setTransform(angle_cosine, angle_sine, -angle_sine, angle_cosine, x0, y0);
    ctx.setTransform(1, 0, 0, -1, x0, y0); // Flip vertically
}

function drawAxis (canvas) {
    let ctx = canvas.getContext ("2d")

    console.log (ctx)
    let x0 = canvas.width /2
    let y0 = canvas.height /2
    let ww = canvas.width/2
    let hh = canvas.height/2

    setTransform (ctx, x0, y0)

    ctx.beginPath ()
    ctx.fillStyle = "lightgray"
    ctx.fillRect(-ww, -hh, canvas.width, canvas.height)
    ctx.stroke ()

    ctx.beginPath ()
    ctx.strokeStyle = "black"
    ctx.moveTo(- ww, 0)
    ctx.lineTo(ww*2, 0)
    ctx.moveTo(0, -hh)
    ctx.lineTo(0, hh*2)
    ctx.stroke ()
}

function drawFunction (canvas, func) {
    console.log ("drawFunction: " + func)
    let ctx = canvas.getContext ("2d")

    drawAxis (canvas)

    let x0 = canvas.width /2
    let y0 = canvas.height /2
    let ww = canvas.width/2
    let hh = canvas.height/2

    setTransform (ctx, x0, y0)

    // Plot functionl
    ctx.beginPath ()
    ctx.strokeStyle = "blue"
    for (let xx = -ww; xx < ww; ++xx) {
 	let yy = func (xx*scale_x)
	ctx.lineTo(xx, yy*scale_y)
    }
    ctx.stroke ()
}

function round5(number) {
  return Math.round (number * 10000) / 10000
}

function drawNewtonsMethod (canvas, func, derivative,initial_x, precision) {
    let ctx = canvas.getContext ("2d")

    let x0 = canvas.width /2
    let y0 = canvas.height /2
    let ww = canvas.width/2
    let hh = canvas.height/2

    setTransform (ctx, x0, y0)

    //  Plot successive iterations of Newton's method
    let xn = initial_x
    let yy = func(xn*scale_x)

    ctx.beginPath ()
    ctx.strokeStyle = "purple"
    ctx.textStyle = "purple"
    marker (ctx, xn, yy*scale_y, 0)
    ctx.stroke ()

    ctx.beginPath ()
    ctx.strokeStyle = "red"
    ctx.textStyle = "red"

    for (let count = 1; count < 300; ++ count) {
	console.log (count + " xx=" + xn + " yy=" + yy)
	marker (ctx, xn, yy*scale_y, count)
	document.getElementById ("message").innerHTML = "Found root at:  x=" + round5(xn) + " after " + count + " iterations (actual y=" + round5(yy) + ")."
	xnn = xn - yy/derivative(xn*scale_x)
	let ynext = func(xnn*scale_x)
	if (Math.abs(ynext) < precision) break;
	yy = ynext
	xn = xnn
    }
    ctx.stroke ()
}

function marker (ctx, xx, yy, text) {
    let ww =  6
    let ww2 = ww*2
    ctx.rect(xx - ww, yy - ww, ww2, ww2)
    ctx.fillText (text, xx - ww +1, yy +ww-1)
}
