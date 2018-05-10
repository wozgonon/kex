import java.util.Stack;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.function.UnaryOperator;
import java.util.function.BinaryOperator;

/**
 *  A little Reverse Polish Notation calculator (cf Forth, Postscript)
 * to demonstrate the Java 8 Lambda's
 *
 * java DoLambda 1 2 neg neg add 4 mul pi cos pi sin pi tan inf neg
 * java RPN /sqr dup mul def 2 sqr
 */

public class RPN
{
    static final HashMap<String, String []>              functions = new HashMap<String, String []> ();
    static final HashMap<String, UnaryOperator<Double>>  unary     = new HashMap<String, UnaryOperator<Double>> ();
    static final HashMap<String, BinaryOperator<Double>> binary    = new HashMap<String, BinaryOperator<Double>> ();
    static final Stack<Object>                           stack     = new Stack<Object> ();

    public static void main (String [] args)
    {
	functions.put   ("inf", new String [] { Double.toString (Double.POSITIVE_INFINITY) });
	functions.put   ("pi",  new String [] { Double.toString (Math.PI) });
	functions.put   ("e",   new String [] { Double.toString (Math.E) });
	unary.put  ("neg", x -> -x);             // Unary Lambda
	unary.put  ("exp", x -> Math.exp (x));
	unary.put  ("cos", x -> Math.cos (x));
	unary.put  ("sin", x -> Math.sin (x));
	unary.put  ("tan", x -> Math.tan (x));
	binary.put ("add", (x, y) -> x + y);     // Binary Lambda
	binary.put ("sub", (x, y) -> x - y);
	binary.put ("div", (x, y) -> x / y);
	binary.put ("mul", (x, y) -> x * y);
	binary.put ("mod", (x, y) -> x % y);
	binary.put ("pow", (x, y) -> Math.pow (x,y));

	run (args);
	//stack.stream ().forEach (System.out::print);
	for (double value : stack) {
	    System.out.format ("%f ", value);
	}
	System.out.format ("\n");
    }
    static void run (String [] args) {
	for (int xx = 0; xx < args.length; ++ xx) {
	    final String arg = args [xx].intern ();
	    if (arg == "dup") {
		stack.push (stack.peek ());
		continue;
	    }
	    if (arg == "exch") {
		final double top  = stack.peek ();
		final double next = stack.peek ();
		stack.push (top);
		stack.push (next);
		continue;
	    }
	    if (arg == "if") {
		stack.push (stack.peek ());
		continue;
	    }
	    final String [] function = functions.get (arg);
	    if (function != null) {
		run (function);
		continue;
	    }
	    final BinaryOperator<Double> bop = binary.get (arg);
	    if (bop != null) {
		stack.push (bop.apply (stack.pop(), stack.pop()));
		continue;
	    }
	    UnaryOperator<Double> uop;
	    if ((uop = unary.get (arg)) != null) {  // Just to demonstrate one can assign in an 'if' statement
		stack.push (uop.apply (stack.pop()));
		continue;
	    }
	    if (arg.startsWith ("{")) {
		final ArrayList<String> definition = new ArrayList<String> ();
		for (++ xx; xx < args.length; ++ xx) {
		    final String arg1 = args [xx].intern ();
		    if (arg1 == "}") break;
		    definition.add (arg1);
		}
		stack.push (definition.toArray (new String [] {}));
		continue;
	    }
	    if (arg.startsWith ("/")) {
		final String            name       = arg.substring (1);
		final ArrayList<String> definition = new ArrayList<String> ();
		for (++ xx; xx < args.length; ++ xx) {
		    final String arg1 = args [xx].intern ();
		    if (arg1 == "def") break;
		    definition.add (arg1);
		}
		functions.put (name, definition.toArray (new String [] {}));
		continue;
	    }
	    stack.push (Double.valueOf (arg));
	}
    }
}
