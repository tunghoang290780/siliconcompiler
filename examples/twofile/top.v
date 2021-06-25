module top
(
  input  wire clk,
  output reg [3:0] out
);

  counter counter (
    .clk(clk),
    .out(out)
  );

endmodule 
