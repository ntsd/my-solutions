using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;

class Path
{
    public int cost;
    public List<Point> path;
    public Point next;
    
    public Path(int cost, Point next, List<Point> path){
        this.cost = cost;
        this.next = next;
        this.path = path;
    }
}

class Heap
{
    public int count = 0;
    public SortedList<int, Path> paths = new SortedList<int, Path>();

    public void Add(Path path){
        this.paths.Add(path.cost, path);
        this.count++;
    }
    
    public Path Pop(){
        Path path = paths[0];
        paths.RemoveAt(0);
        count--;
        return path;
    }
}

class Point
{
    public int x { get; set; }
    public int y { get; set; }
    
    public Point(int x, int y)
    {
        this.x = x;
        this.y = y;
    }
    
    public override bool Equals(Object obj) 
    {
        if (obj == null || GetType() != obj.GetType()) 
         return false;
        
        Point p = (Point)obj;
        return (this.x == p.x) && (this.y == p.y);
    }
    
    public override int GetHashCode() 
    {
        return  this.x ^ this.y;
    }
}


class Wall: Point
{
    public string orientation { get; set; }
    
    public Wall(int x, int y, string orientation): base(x, y)
    {
        this.orientation = orientation;
    }
    
    public bool isCross(Wall other){
        if(this.orientation == other.orientation && this.x == other.x && this.y == other.y)return true;
        if(this.orientation.Equals('V') && other.orientation.Equals('V') && this.x == other.x && Math.Abs(this.y-other.y)<2)return true;
        if(this.orientation.Equals('H') && other.orientation.Equals('H') && this.y == other.y && Math.Abs(this.x-other.x)<2)return true;
        if(this.orientation != other.orientation){
            if(this.orientation.Equals('H') && this.x==other.x+1 && this.y==other.y-1)return true;
            else if(this.orientation.Equals('V') && this.x==other.x-1 && this.y==other.y+1)return true;
        }
        return false;
    }
    
    public override bool Equals(Object obj) 
    {
        return base.Equals(obj) && orientation == ((Wall)obj).orientation;
    }
    
    public override int GetHashCode() 
    {
        return base.GetHashCode() ^ orientation.GetHashCode();
    }
}

class Player
{
    public int id { get; set; }
    public int x { get; set; }
    public int y { get; set; }
    public int walls_left { get; set; }
    List<Point> targets { get; set; }
    
    public Player(int id, List<Point> targets)
    {
       this.id = id;
       this.targets = targets;
    }
    
    public void update(string[] inputs)
    {
        this.x = int.Parse(inputs[0]);
        this.y = int.Parse(inputs[1]);
        this.walls_left = int.Parse(inputs[2]);
    }
    
    public Path shortest_path_closet(Dictionary<Point, List<Point>> graph, List<Point> ends){
        Heap heapq = new Heap();
        heapq.Add(new Path(0, new Point(this.x, this.y), new List<Point>()));
        HashSet<Point> seen = new HashSet<Point>();
        Path path;
        while(heapq.count > 0){
            path = heapq.Pop();
            if(!seen.Contains(path.next)){
                path.path.Add(path.next);
                seen.Add(path.next);
                if(ends.Contains(path.next))return path;
                foreach(Point next in graph[path.next]){
                    heapq.Add(new Path(path.cost+1, next, path.path));
                }
            }
        }
        return null;// return null if not see path
    }
}


class Program
{
    static string action(){
        return "RIGHT";
    }
    
    static void Main(string[] args)
    {
        string[] inputs;
        inputs = Console.ReadLine().Split(' ');
        int w = int.Parse(inputs[0]); // width of the board
        int h = int.Parse(inputs[1]); // height of the board
        int playerCount = int.Parse(inputs[2]); // number of players (2 or 3)
        int myId = int.Parse(inputs[3]); // id of my player (0 = 1st player, 1 = 2nd player, ...)
        
        Dictionary<Point, List<Point>> graph = new Dictionary<Point, List<Point>>();
        List<List<Point>> targets = new List<List<Point>>()
        {new List<Point>(), new List<Point>(), new List<Point>()};
        
        foreach (int y in Enumerable.Range(0,h))
        {
            foreach (int x in Enumerable.Range(0,w))
            {
                List<Point> neighbours = new List<Point>();
                if(x < w-1)neighbours.Add(new Point(x + 1, y));
                else targets[0].Add(new Point(x, y));
                if(x > 0)neighbours.Add(new Point(x - 1, y));
                else targets[1].Add(new Point(x, y));
                if(y < h-1)neighbours.Add(new Point(x, y + 1));
                else targets[2].Add(new Point(x, y));
                if(y > 0)neighbours.Add(new Point(x, y - 1));
                graph.Add(new Point(x, y), neighbours);
            }
        }
        
        List<Player> players = new List<Player>();
        foreach (int i in Enumerable.Range(0,playerCount))
        {
            players.Add(new Player(i, targets[i]));
        }
        
        List<Wall> walls = new List<Wall>();
        
        while (true)// game loop
        {
            foreach(Player player in players){
                player.update(Console.ReadLine().Split(' '));
            }
            
            int wallCount = int.Parse(Console.ReadLine());
            for (int i = 0; i < wallCount; i++)
            {
                inputs = Console.ReadLine().Split(' ');
                int wall_x = int.Parse(inputs[0]);
                int wall_y = int.Parse(inputs[1]);
                string orientation = inputs[2]; // ('H' or 'V')
                Wall wall = new Wall(wall_x, wall_y, orientation);
                if(walls.Exists(w_ => w_.isCross(wall))){
                    if(orientation.Equals('H')){
                        graph[new Point(wall_x, wall_y)].Remove(new Point(wall_x, wall_y-1));
                        graph[new Point(wall_x, wall_y-1)].Remove(new Point(wall_x, wall_y));
                        graph[new Point(wall_x+1, wall_y)].Remove(new Point(wall_x+1, wall_y-1));
                        graph[new Point(wall_x+1, wall_y-1)].Remove(new Point(wall_x+1, wall_y));
                    }
                    else if(orientation.Equals('V')){
                        graph[new Point(wall_x, wall_y)].Remove(new Point(wall_x-1, wall_y));
                        graph[new Point(wall_x-1, wall_y)].Remove(new Point(wall_x, wall_y));
                        graph[new Point(wall_x, wall_y+1)].Remove(new Point(wall_x-1, wall_y+1));
                        graph[new Point(wall_x-1, wall_y+1)].Remove(new Point(wall_x, wall_y+1));
                    }
                    walls.Add(wall);
                }
            }

            Console.WriteLine(action());
        }
    }
}