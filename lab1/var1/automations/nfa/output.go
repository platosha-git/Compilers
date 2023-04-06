package nfa

//
//digraph regexp {
//fontname="Helvetica,Arial,sans-serif"
//node [fontname="Helvetica,Arial,sans-serif"]
//edge [fontname="Helvetica,Arial,sans-serif"]
//n0 [label="regexp", URL="https://godoc.org/regexp", tooltip="Package regexp implements regular expression search."];
//n1 [label="bytes", URL="https://godoc.org/bytes", tooltip="Package bytes implements functions for the manipulation of byte slices."];
//n2 [label="io", URL="https://godoc.org/io", tooltip="Package io provides basic interfaces to I/O primitives."];
//n3 [label="regexp/syntax", URL="https://godoc.org/regexp/syntax", tooltip="Package syntax parses regular expressions into parse trees and compiles parse trees into programs."];
//n4 [label="sort", URL="https://godoc.org/sort", tooltip="Package sort provides primitives for sorting slices and user-defined collections."];
//n5 [label="strconv", URL="https://godoc.org/strconv", tooltip="Package strconv implements conversions to and from string representations of basic data types."];
//n6 [label="strings", URL="https://godoc.org/strings", tooltip="Package strings implements simple functions to manipulate UTF-8 encoded strings."];
//n7 [label="sync", URL="https://godoc.org/sync", tooltip="Package sync provides basic synchronization primitives such as mutual exclusion locks."];
//n8 [label="unicode", URL="https://godoc.org/unicode", tooltip="Package unicode provides data and functions to test some properties of Unicode code points."];
//n9 [label="unicode/utf8", URL="https://godoc.org/unicode/utf8", tooltip="Package utf8 implements functions and constants to support text encoded in UTF-8."];
//n10 [label="internal/bytealg", URL="https://godoc.org/internal/bytealg", tooltip=""];
//n11 [label="errors", URL="https://godoc.org/errors", tooltip="Package errors implements functions to manipulate errors."];
//n12 [label="internal/reflectlite", URL="https://godoc.org/internal/reflectlite", tooltip="Package reflectlite implements lightweight version of reflect, not using any package except for \"runtime\" and \"unsafe\"."];
//n13 [label="math", URL="https://godoc.org/math", tooltip="Package math provides basic constants and mathematical functions."];
//n14 [label="math/bits", URL="https://godoc.org/math/bits", tooltip="Package bits implements bit counting and manipulation functions for the predeclared unsigned integer types."];
//n15 [label="unsafe", URL="https://godoc.org/unsafe", tooltip="Package unsafe contains operations that step around the type safety of Go programs."];
//n16 [label="internal/race", URL="https://godoc.org/internal/race", tooltip="Package race contains helper functions for manually instrumenting code for the race detector."];
//n17 [label="runtime", URL="https://godoc.org/runtime", tooltip=""];
//n18 [label="sync/atomic", URL="https://godoc.org/sync/atomic", tooltip="Package atomic provides low-level atomic memory primitives useful for implementing synchronization algorithms."];
//n19 [label="internal/cpu", URL="https://godoc.org/internal/cpu", tooltip="Package cpu implements processor feature detection used by the Go standard library."];
//n0 -> n1;
//n0 -> n2;
//n0 -> n3;
//n0 -> n4;
//n0 -> n5;
//n0 -> n6;
//n0 -> n7;
//n0 -> n8;
//n0 -> n9;
//n1 -> n10;
//n1 -> n2;
//n1 -> n8;
//n1 -> n9;
//n1 -> n11;
//n2 -> n11;
//n2 -> n7;
//n3 -> n4;
//n3 -> n5;
//n3 -> n6;
//n3 -> n8;
//n3 -> n9;
//n4 -> n12;
//n5 -> n10;
//n5 -> n13;
//n5 -> n9;
//n5 -> n11;
//n5 -> n14;
//n6 -> n2;
//n6 -> n7;
//n6 -> n15;
//n6 -> n11;
//n6 -> n10;
//n6 -> n8;
//n6 -> n9;
//n7 -> n16;
//n7 -> n17;
//n7 -> n18;
//n7 -> n15;
//n10 -> n19;
//n10 -> n15;
//n11 -> n12;
//n12 -> n17;
//n12 -> n15;
//n13 -> n15;
//n13 -> n19;
//n13 -> n14;
//n14 -> n15;
//n16 -> n15;
//n18 -> n15;
//}