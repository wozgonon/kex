class Pad {
    constructor (id) {
	this.canvas = document.getElementById(id)
	this.ctx = this.canvas.getContext("2d")
    }
    drawBar (index, value) {
	let canvas = this.canvas
	let ctx = this.ctx
	const WW=10
	const SPACE = 5
	//console.log (value)
	let xx = index * (WW + SPACE)
	let yy = canvas.height-value
	let ww = WW
	let hh = value
	ctx.beginPath()
	ctx.fillStyle = "#FFFFFF"
	ctx.strokeStyle = "#FFFFFF"
	ctx.fillRect(xx, 0, ww, canvas.height)
	ctx.rect    (xx, 0, ww, canvas.height)
	ctx.stroke()
	ctx.beginPath()
	ctx.fillStyle = "#FF0000"
	ctx.fillRect(xx, yy, ww, hh)
	ctx.stroke()
	ctx.beginPath()
	ctx.strokeStyle = "#444444"
	ctx.rect(xx, yy, ww, hh)
	ctx.stroke()
    }
    drawArray (array) {
	for (let ii = 0; ii < array.length; ++ ii) {
	    this.drawBar (ii, array [ii])
	}
    }
}

function bag (max) {
    let pad = new Pad("bag")
    let array = []
    for (let ii = 0; ii < max; ++ ii) {
	let number = Math.floor (Math.random ()*max)
	array [ii] = number
	pad.drawBar(ii, array [ii])
    }
    return array
}

/**
  *   A visual bubble sort
  *
  */

function bubble (array) {
    let pad = new Pad("bubble")
    let len = array.length
    pad.drawArray(array)
    let change = false
    do {
	change = false
	for (let ii = 0; ii < len; ++ ii) {
	    let rr = ii+1
	    if (rr == len) {
		break;
	    }
	    if (array [ii] > array [rr]) {
		change = true
		let swap = array [rr]
		array [rr] = array [ii]
		array [ii] = swap
		//console.log ("Change: ii=" + ii + " rr=" + rr + " array[ii]=" +array[ii]  + " array[rr]=" +array[rr])
		pad.drawBar(rr, array [rr])
		pad.drawBar(ii, array [ii])
	    }
	    //sleep(100)
	}
    } while (change)
    return array
}

function integer_sort (input_array) {
    let len = input_array.length
    let counters = arrayOfZero (len)
    {
	let pad = new Pad("integer_counters")
	pad.drawArray(counters)
	for (let ii = 0; ii < len; ++ ii) {
	    let rr = input_array [ii]
	    counters [rr] += 1
	    pad.drawBar(rr, counters [rr])
	}
    }
    let array = arrayOfZero (len)
    let count = 0
    let pad = new Pad("integer")
    for (let ii = 0; ii < len; ++ ii) {
	let value = counters [ii]
	for (let jj = 0; jj < value; ++ jj) {
	    array [count] = ii
	    pad.drawBar(count, array [count])
	    count = count + 1
	}
    }
    return array
}

function arrayOfZero (max) {
      let array = []
      for (let ii = 1; ii < max; ++ ii) {
	  array.push (0)
      }
      return array
}

function runBag () {
    array = bag(40)
    array = bubble(array)
    array = integer_sort(array)
}
