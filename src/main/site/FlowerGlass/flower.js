
function multiply_color (color, factor) {
    let hex = color.substring(1, color.length)
    let number = Math.round (parseInt (hex, 16) * factor)
    let string = number.toString (16)
    let result  = "#" + "0".repeat (6 - string.length) + string
    return result
}

class Pad {
    constructor (ID) {
	this.canvas = document.getElementById (ID)
	this.ctx = this.canvas.getContext("2d")
    }
    clear () {
	this.ctx.beginPath ()
	this.ctx.fillStyle = "#FFFFFF"
	this.ctx.fillRect (0, 0, this.canvas.width, this.canvas.height)
	this.ctx.stroke()
    }
}
class Flower {
    constructor (pad, width_factor, angle_factor, length_factor, color_factor) {
	this.pad = pad
	this.width_factor = width_factor
	this.angle_factor = angle_factor
	this.length_factor = length_factor
	this.color_factor = color_factor
	this.rotation = - Math.PI/2
    }
    bifurcate (x, y, width, radius, angle, color, n) {
	if (n <= 0) {
	    return
	}
	//console.log ("x=" + x + " y=" + y + " radius=" + radius + " angle=" + angle + " width=" + width)
	//console.log (color)
	//console.log (this.color_factor)
	this.pad.ctx.beginPath ()
	let x1 = x + radius * Math.cos (angle + this.rotation)
	let y1 = y + radius * Math.sin (angle + this.rotation)
	this.pad.ctx.lineWidth = width
	this.pad.ctx.strokeStyle = color
	this.pad.ctx.moveTo (x, y)
	this.pad.ctx.lineTo (x1, y1)
	//this.pad.ctx.rect (x, y, x1-x, y1-y )
	this.pad.ctx.stroke ()

	let next_color = multiply_color (color, this.color_factor)
	this.bifurcate (x1, y1, width * this.width_factor, radius*this.length_factor, -angle*this.angle_factor, next_color, n-1)
	this.pad.ctx.moveTo (x, y)
	this.bifurcate (x1, y1, width * this.width_factor, radius*this.length_factor, angle*this.angle_factor, next_color, n-1)

    }
}
