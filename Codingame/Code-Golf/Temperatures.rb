gets
puts gets.split(" ").map(&:to_i).min_by{|x|2*x*x-x}||0