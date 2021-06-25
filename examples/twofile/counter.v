module counter (
    input clk,
    output reg [3:0] out
);

always @(posedge clk) begin
    out <= out + 1'b1;
end

endmodule