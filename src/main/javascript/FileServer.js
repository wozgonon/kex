/// A simple web server that serves static files implemented for nodejs
/// > nodejs FileServer.js

port = 8889
dir  = "."

let fs   = require('fs')
let http = require('http')
let url  = require('url')

let server = http.createServer (function (req, res) {
    let parsed_url = url.parse (req.url,true)
    let pathname = parsed.pathname
    let filePath = dir + .pathname
    let stat = fs.lstatSync (filePath)
    if (stat.isDirectory (filePath)) {
	fs.readdir(filePath, err, files) => {
	    if (err === null) {
		res.writeHead (200, {'ContentType': 'text/html'})
		res.write ("<html><body>")
		files.foreach (file => {
		    let fileName = file.toString ()
		    let prefix = pathname == "/" ? "" : pathname
		    let path = prefix + fileName
		    res.write ("<li><a href=\"" + path + "\">" + fileName + "</a>")
		})
		res.write ("</body></html>")
	    } else {
		res.writeHead (404, {'ContentType': 'text/html'})
		res.write (err.toString ())
	    }
	    res.end()
	}
    } else { // if (stat.isFile (filePath)) {
	fs.readFile (filePath, function (err, data) {
	    if (err === null) {
		res.writeHead (200, {'ContentType': 'text/html'})
		res.write (data.toString ())
	    } else {
		res.writeHead (404, {'ContentType': 'text/html'})
		res.write (err.toString ())
	    }
	    res.end()
	});
    }

});

server.listen (port)
