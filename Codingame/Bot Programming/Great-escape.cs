using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;

using System.Runtime.Serialization.Formatters.Binary;
// height=9
// positions=8 1 1 4
// width=9
// symmetric=false

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
    
    public override string ToString()
    {
        if(this.path.Count > 0)return String.Format("(cost:{0},this:{1},next:{2})",this.cost, this.path[this.path.Count-1], this.next);
        return String.Format("(cost:{0},next:{1})",this.cost, this.next);
    }
}

class HeapQueue // don't use anymore
{
    public int count;
    public int index;
    public SortedList<int, Path> paths;
    
    public HeapQueue()
    {
        count = 0;
        index = 0;
        paths = new SortedList<int, Path>();
    }
    
    public void Add(Path path){
        // Console.Error.WriteLine(path.ToString());
        this.paths.Add(path.cost*1000000+this.index, path);
        this.count++;
        this.index++;
    }
    
    public Path Pop(){
        Path path = paths[paths.Keys[0]]; // get frist element
        // Console.Error.WriteLine(path.ToString());
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
    
    public override string ToString()
    {
        return String.Format("({0},{1})",this.x, this.y);
    }
}


class Wall: Point
{
    public string orientation { get; set; }
    
    public Wall(int x, int y, string orientation): base(x, y)
    {
        this.orientation = orientation;
    }
    
    public bool IsCross(Wall other){
        if(this.orientation.Equals(other.orientation) && this.x == other.x && this.y == other.y)return true;
        if(this.orientation.Equals("V") && other.orientation.Equals("V") && this.x == other.x && Math.Abs(this.y-other.y)<2)return true;
        if(this.orientation.Equals("H") && other.orientation.Equals("H") && this.y == other.y && Math.Abs(this.x-other.x)<2)return true;
        if(this.orientation.Equals(other.orientation)){
            if(this.orientation.Equals("V") && this.x==other.x+1 && this.y==other.y-1)return true;
            if(this.orientation.Equals("H") && this.x==other.x-1 && this.y==other.y+1)return true;
        }
        return false;
    }
    
    public override bool Equals(Object obj) 
    {
        return base.Equals(obj) && orientation.Equals(((Wall)obj).orientation);
    }
    
    public override int GetHashCode() 
    {
        return base.GetHashCode() ^ orientation.GetHashCode();
    }
    
    public override string ToString()
    {
        return String.Format("({0},{1},{2})",this.x, this.y, this.orientation);
    }
}

class Player
{
    public int id { get; set; }
    public int x { get; set; }
    public int y { get; set; }
    public int wallsLeft { get; set; }
    public List<Point> targets { get; set; }
    
    public Player(int id, List<Point> targets)
    {
        this.id = id;
        this.targets = targets;
        // Console.Error.WriteLine(id.ToString() +' '+ targets[0].ToString());
    }
    
    public void Update(string[] inputs)
    {
        this.x = int.Parse(inputs[0]);
        this.y = int.Parse(inputs[1]);
        this.wallsLeft = int.Parse(inputs[2]);
    }
    
    public Path ShortestPathCloset(Dictionary<Point, List<Point>> graph){
        Queue<Path> queue = new Queue<Path>();
        queue.Enqueue(new Path(0, new Point(this.x, this.y), new List<Point>()));
        HashSet<Point> seen = new HashSet<Point>();
        while(queue.Count > 0){
            Path path_ = queue.Dequeue();
            // Console.Error.WriteLine(path_.ToString());
            if(!seen.Contains(path_.next)){
                List<Point> new_path = path_.path.ToList(); // use ToList to clone list<point>
                new_path.Add(path_.next);
                seen.Add(path_.next);
                if(this.targets.Contains(path_.next)){
                    path_.path = new_path;
                    return path_;
                }
                // foreach(Point t in this.targets){
                //     if(t.x == path_.next.x && t.y==path_.next.y)return path_;
                // }
                foreach(Point next in graph[path_.next]){
                    queue.Enqueue(new Path(path_.cost+1, next, new_path));
                }
            }
        }
        return null;// return null if not see path
    }
    
    public int Score(Dictionary<Point, List<Point>> graph){
        Path shortestPath = this.ShortestPathCloset(graph);
        if(shortestPath == null)return -1; // no way to target
        return shortestPath.cost;
    }
    
    
    public string GetDirection(Point next_point){
        if(next_point.x < this.x)return "LEFT";
        if(next_point.x > this.x)return "RIGHT";
        if(next_point.y < this.y)return "UP";
        if(next_point.y > this.y)return "DOWN";
        return "NONE";
    }
}

class Program
{

    static string action(Player myPlayer, List<Player> opPlayer, Dictionary<Point, List<Point>> graph, List<Wall> walls, int h, int w){
        
        Path myShortestPath = myPlayer.ShortestPathCloset(graph);
        // Console.Error.WriteLine(myShortestPath.cost.ToString() +' '+ myShortestPath.path[1].ToString());
        int oldMyScore = myShortestPath.cost;
        int oldOpScore = 0;
        foreach(Player op in opPlayer){
            oldOpScore += op.Score(graph);
        }
        
        if(myPlayer.wallsLeft > 0){
            Wall bestWall = null;
            int bestScore = 0;
            foreach(int wall_y in Enumerable.Range(1,h-1)){
                foreach(int wall_x in Enumerable.Range(0,w-1)){
                    Wall wall = new Wall(wall_x, wall_y, "H");
                    // Console.Error.WriteLine((Point)wall);
                    if(!walls.Exists(w_ => w_.IsCross(wall))){
                        Dictionary<Point, List<Point>> graph_temp = graph.ToDictionary(entry => entry.Key, 
                                               entry => entry.Value.ToList()); // to deep copy
                        graph_temp[new Point(wall_x, wall_y)].Remove(new Point(wall_x, wall_y-1));
                        graph_temp[new Point(wall_x, wall_y-1)].Remove(new Point(wall_x, wall_y));
                        graph_temp[new Point(wall_x+1, wall_y)].Remove(new Point(wall_x+1, wall_y-1));
                        graph_temp[new Point(wall_x+1, wall_y-1)].Remove(new Point(wall_x+1, wall_y));
                        int newMyScore = myPlayer.Score(graph_temp);
                        if(oldMyScore >= newMyScore){ // to check that not reduce own path
                            int opScore = 0;
                            foreach(Player op in opPlayer){
                                opScore += op.Score(graph_temp);
                            }
                            if(opScore > oldOpScore && opScore > bestScore){
                                bestScore = opScore;
                                bestWall = wall;
                            }
                        }
                    }
                }
            }
            foreach(int wall_y in Enumerable.Range(0,h-1)){
                foreach(int wall_x in Enumerable.Range(1,w-1)){
                    Wall wall = new Wall(wall_x, wall_y, "V");
                    //Console.Error.WriteLine((Point)wall);
                    if(!walls.Exists(w_ => w_.IsCross(wall))){
                        Dictionary<Point, List<Point>> graph_temp = graph.ToDictionary(entry => entry.Key, 
                                               entry => entry.Value.ToList()); // to deep copy
                        graph_temp[new Point(wall_x, wall_y)].Remove(new Point(wall_x-1, wall_y));
                        graph_temp[new Point(wall_x-1, wall_y)].Remove(new Point(wall_x, wall_y));
                        graph_temp[new Point(wall_x, wall_y+1)].Remove(new Point(wall_x-1, wall_y+1));
                        graph_temp[new Point(wall_x-1, wall_y+1)].Remove(new Point(wall_x, wall_y+1));
                        int newMyScore = myPlayer.Score(graph_temp);
                        if(oldMyScore >= newMyScore){ // to check that not reduce own path
                            int opScore = 0;
                            foreach(Player op in opPlayer){
                                opScore += op.Score(graph_temp);
                            }
                            if(opScore > oldOpScore && opScore > bestScore){
                                bestScore = opScore;
                                bestWall = wall;
                            }
                        }
                    }
                }
            }
            if(bestWall != null){
                return String.Format("{0} {1} {2}",bestWall.x, bestWall.y, bestWall.orientation );
            }
        }
        return myPlayer.GetDirection(myShortestPath.path[1]);
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
                // Console.Error.WriteLine(x.ToString()+y.ToString());
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
                player.Update(Console.ReadLine().Split(' '));
            }
            
            int wallCount = int.Parse(Console.ReadLine());
            for (int i = 0; i < wallCount; i++)
            {
                inputs = Console.ReadLine().Split(' ');
                int wall_x = int.Parse(inputs[0]);
                int wall_y = int.Parse(inputs[1]);
                string orientation = inputs[2]; // ('H' or 'V')
                Wall wall = new Wall(wall_x, wall_y, orientation);
                // foreach(Wall w_ in walls){ //to debug wall
                //     if(wall.IsCross(w_)){
                //         Console.Error.WriteLine(wall.ToString()+w_.ToString());
                //     }
                // }
                if(!walls.Exists(w_ => w_.IsCross(wall))){
                    if(orientation.Equals("H")){
                        graph[new Point(wall_x, wall_y)].Remove(new Point(wall_x, wall_y-1));
                        graph[new Point(wall_x, wall_y-1)].Remove(new Point(wall_x, wall_y));
                        graph[new Point(wall_x+1, wall_y)].Remove(new Point(wall_x+1, wall_y-1));
                        graph[new Point(wall_x+1, wall_y-1)].Remove(new Point(wall_x+1, wall_y));
                    }
                    else if(orientation.Equals("V")){
                        // Console.Error.WriteLine("wall add");
                        graph[new Point(wall_x, wall_y)].Remove(new Point(wall_x-1, wall_y));
                        graph[new Point(wall_x-1, wall_y)].Remove(new Point(wall_x, wall_y));
                        graph[new Point(wall_x, wall_y+1)].Remove(new Point(wall_x-1, wall_y+1));
                        graph[new Point(wall_x-1, wall_y+1)].Remove(new Point(wall_x, wall_y+1));
                    }
                    // Console.Error.WriteLine(wall);
                    walls.Add(wall);
                }
            }
            
            Player myPlayer = players[myId];
            List<Player> opPlayer = players.Where( p => p.id != myId && p.x != -1).ToList();
            
            string output = action(myPlayer, opPlayer, graph, walls, h, w);
            Console.WriteLine(output);
        }
    }}