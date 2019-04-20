import java.util.*;
import java.io.*;
import java.math.*;

class Globals {
    public static Random rand = new Random();
    public static final int CP  = 0;
    public static final int POD = 1;
    public static final int DEPTH = 6;
    public static final double SHIELD_PROB = 10;
    public static final int MAX_THRUST = 100;
    
    public static final double E = 0.00001;
    
    public static int r = -1;
    public static int turn = 0;
    public static int sols_ct = 0;
    public static boolean is_p2 = false;
    public static int cp_ct;
    public static int laps;
    
    public static Pod[] pods;
    public static Checkpoint[] cps;

    public static long now;
    public static long TIME() { // Todo
        return System.currentTimeMillis() - now;
    }
    
    static void print_move(int thrust, double angle, Pod pod) {
        double a = pod.angle + angle;
    
        if (a >= 360.0) {
            a = a - 360.0;
        } else if (a < 0.0) {
            a += 360.0;
        }
    
        a = a * Math.PI / 180.0;
        double px = pod.x + Math.cos(a) * 10000.0;
        double py = pod.y + Math.sin(a) * 10000.0;
    
        if (thrust == -1) {
            System.out.printf("%d %d SHIELD %s\n", (int) Math.round(px), (int) Math.round(py));
            pod.shield = 4;
        } else if (thrust == 650) {
            pod.has_boost = 0;
            System.out.printf("%d %d BOOST %s\n", (int) Math.round(px), (int) Math.round(py));
        } else {
            System.out.printf("%d %d %d %s\n", (int) Math.round(px), (int) Math.round(py), thrust);
        }
    }
    
    static int rnd(int n) {
        return rand.nextInt(n);
    }
    
    static int rnd(int min, int max) {
        return rand.nextInt((max - min) + 1) + min;
    }
}

enum UnitType {
    POD, CHECKPOINT
}


class Point {
    double x;
    double y;
    
    Point() {
    }
    
    Point(double x, double y) {
        this.x  = x;
        this.y  = y;
    }
    
    double dist(Point p) {
        return Math.sqrt(Math.pow((this.x - p.x), 2) + Math.pow((this.y - p.y), 2));
    }
}


class Unit extends Point {
    double[] cache = new double[4];
    int id;
    UnitType type;
    double r;
    double vx;
    double vy;
    
    static double E = 0.00001;
    
    double collision_time(Unit u) {
        if (vx == u.vx && vy == u.vy) {
            return -1;
        }

        double sr2 = u.type == UnitType.CHECKPOINT ? 357604 : 640000;

        double dx = x - u.x;
        double dy = y - u.y;
        double dvx = vx - u.vx;
        double dvy = vy - u.vy;
        double a = dvx*dvx + dvy*dvy;

        if (a < E) return -1;

        double b = -2.0 * (dx * dvx + dy * dvy);
        double delta = b*b - 4.0 * a * (dx * dx + dy * dy - sr2);

        if (delta < 0.0) return -1;

        double t = (b - Math.sqrt(delta))*(1.0/(2.0*a));

        if (t <= 0.0 || t > 1.0) return -1;

        return t;
    }
    
    void save() {
        cache[0] = this.x;
        cache[1] = this.y;
        cache[2] = this.vx;
        cache[3] = this.vy;
    }

    void load() {
        this.x = cache[0];
        this.y = cache[1];
        this.vx = cache[2];
        this.vy = cache[3];
    }
    
    void bounce(Unit u) {
    }
}


class Collision {
    Unit a;
    Unit b;
    double t;

    Collision() {}

    Collision(Unit a, Unit b, double t) {
        this.a = a;
        this.b = b;
        this.t = t;
    }
};

class Checkpoint extends Unit { 
    Checkpoint(int id, double x, double y) {
        this.id = id;
        this.x = x;
        this.y = y;

        this.vx = 0;
        this.vy = 0;
        this.type = UnitType.CHECKPOINT;
        this.r = 600;
    }

    void bounce(Unit u) {
    }
}

class Pod extends Unit {
    double angle = -1;
    double next_angle = -1;
    int has_boost;
    int ncpid;
    int checked;
    int timeout;
    int shield;
    Pod partner;
    
    double[] cache = new double[6];
    
    Pod(int id) {
        this.id = id;
        this.r = 400;
        this.type = UnitType.POD;
        this.ncpid = 1;

        this.timeout = 100;
        this.has_boost = 1;
        this.checked = 0;
        this.shield = 0;
    }
    
    double score() {
        return checked*50000 - this.dist(Globals.cps[this.ncpid]);
    }
    
    void apply(int thrust, double angle) {
        angle = Math.max(-18.0, Math.min(18.0, angle));
        this.angle += angle;
        if (this.angle >= 360.0) {
            this.angle = this.angle - 360.0;
        } else if (this.angle < 0.0) {
            this.angle += 360.0;
        }

        if (thrust == -1) {
            this.shield = 4;
        } else {
            boost(thrust);
        }
    }
    
    void rotate(Point p) {
        double a = diff_angle(p);
        a = Math.max(-18.0, Math.min(18.0, a));

        angle += a;
        if (angle >= 360.0) {
            angle = angle - 360.0;
        } else if (angle < 0.0) {
            angle += 360.0;
        }
    }
    
    void boost(int thrust) {
        if (shield > 0) return;

        double ra = angle * Math.PI / 180.0;

        vx += Math.cos(ra) * thrust;
        vy += Math.sin(ra) * thrust;
    }

    void move(double t) {
        x += vx * t;
        y += vy * t;
    }
    
    void end() {
        x = Math.round(x);
        y = Math.round(y);
        vx = vx * 0.85;
        vy = vy * 0.85;

        if (checked >= Globals.cp_ct * Globals.laps) {
            ncpid = 0;
            checked = Globals.cp_ct * Globals.laps;
        }
        timeout--;
        if (shield > 0) shield--;
    }
    
    void bounce(Unit u) {
        if (u.type == UnitType.CHECKPOINT) {
            checked += 1;
            timeout = partner.timeout = 100;
            ncpid = (ncpid + 1) % Globals.cp_ct;
            return;
        }
        bounce_w_pod((Pod) u);
    }

    void bounce_w_pod(Pod u) {
        double m1 = shield == 4 ? 10. : 1.;
        double m2 = u.shield == 4 ? 10. : 1.;
        double mcoeff = (m1 + m2) / (m1 * m2);

        double nx = x - u.x;
        double ny = y - u.y;
        double dst2 = nx*nx + ny*ny;
        double dvx = vx - u.vx;
        double dvy = vy - u.vy;
        double prod = (nx*dvx + ny*dvy) / (dst2 * mcoeff);
        double fx = nx * prod;
        double fy = ny * prod;
        double m1_inv = 1.0 / m1;
        double m2_inv = 1.0 / m2;

        vx -= fx * m1_inv;
        vy -= fy * m1_inv;
        u.vx += fx * m2_inv;
        u.vy += fy * m2_inv;

        double impulse = Math.sqrt(fx*fx + fy*fy);
        if (impulse < 120.) {
            double df = 120.0 / impulse;
            fx *= df;
            fy *= df;
        }

        vx -= fx * m1_inv;
        vy -= fy * m1_inv;
        u.vx += fx * m2_inv;
        u.vy += fy * m2_inv;
    }

    double diff_angle(Point p) {
        double a = get_angle(p);
        double right = angle <= a ? a - angle : 360. - angle + a;
        double left = angle >= a ? angle - a : angle + 360. - a;

        if (right < left) {
            return right;
        }

        return -left;
    }

    double get_angle(Point p) {
        double d = this.dist(p);
        double dx = (p.x - x) / d;
        double dy = (p.y - y) / d;

        double a = Math.acos(dx) * 180 / Math.PI;

        if (dy < 0) {
            a = 360 - a;
        }

        return a;
    }

    void update(int x, int y, int vx, int vy, float angle, int ncpid) {
        if (shield > 0) shield--;
        if (ncpid != this.ncpid) {
            timeout = 100;
            partner.timeout = 100;
            checked++;
        } else {
            timeout--;
        }

        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.ncpid = ncpid;

        if (Globals.is_p2 && id > 1) swap(angle, this.next_angle);
        this.angle = angle;
        if (this.r == 0) this.angle = 1 + diff_angle(Globals.cps[1]);
        save();
    }
    
    void swap(double a, double b){
        double x = a+0;
        a=b+0;
        b=x+0;
    }
    
    void update(int shield, int has_boost) {
        this.shield = shield;
        this.has_boost = has_boost;
    }

    void save() {
        super.save();
        cache[0] = ncpid;
        cache[1] = checked;
        cache[2] = timeout;
        cache[3] = shield;
        cache[4] = angle;
        cache[5] = has_boost;
    }

    void load() {
        super.load();
        ncpid   = (int)cache[0];
        checked = (int)cache[1];
        timeout = (int)cache[2];
        shield  = (int)cache[3];
        angle   = cache[4];
        has_boost = (int)cache[5];
    }
}


// TODO
class Solution {
    double score = -1;
    int[] thrusts = new int[10000]; // TODO cahnge to list
    double[] angles = new double[10000];//[Globals.DEPTH*2]

    Solution(boolean with_rnd) {
        if (with_rnd) randomize();
    }

    void shift() {
        for (int i = 1; i < Globals.DEPTH; i++) {
            angles[i-1]        = angles[i];
            thrusts[i-1]       = thrusts[i];
            angles[i-1+Globals.DEPTH]  = angles[i+Globals.DEPTH];
            thrusts[i-1+Globals.DEPTH] = thrusts[i+Globals.DEPTH];
        }
        randomize(Globals.DEPTH-1, true);
        randomize(2*Globals.DEPTH-1, true);
        score = -1;
    }

    void mutate() {
        randomize(Globals.rnd(2*Globals.DEPTH), false);
    }

    void mutate(Solution child) { // TODO
        // copy(begin(angles), end(angles), begin(child.angles));
        child.angles = angles.clone();
        // copy(begin(thrusts), end(thrusts), begin(child.thrusts));
        child.thrusts = thrusts.clone();

        child.mutate();
        child.score = -1;
    }

    void randomize(int idx, boolean full) {
        int r = Globals.rnd(2);
        if (full || r == 0) angles[idx] = Math.max(-18, Math.min(18, Globals.rnd(-40, 40)));

        if (full || r == 1) {
            if (Globals.rnd(100) >= Globals.SHIELD_PROB) {
                thrusts[idx] = Math.max(0, Math.min(Globals.MAX_THRUST, Globals.rnd((int) -0.5*Globals.MAX_THRUST, 2*Globals.MAX_THRUST)));
            } else {
                thrusts[idx] = -1;
            }
        }
        score = -1;
    }

    void randomize() {
        for (int i = 0; i < 2*Globals.DEPTH; i++) randomize(i, true);
    }
};

//
class Bot {
    int id = 0;

    Bot() {};

    Bot(int id) {
        this.id = id;
    }
    
    void move() {
    }
    
    Pod runner() {
        return runner(Globals.pods[id], Globals.pods[id+1]);
    }

    Pod blocker() {
        return blocker(Globals.pods[id], Globals.pods[id+1]);
    }

    Pod runner(Pod pod0, Pod pod1) {
        if(pod0.score() - pod1.score() >= -1000)return pod0;
        return pod1;
    }

    Pod blocker(Pod pod0, Pod pod1) {
        return runner(pod0, pod1).partner;
    }
};

class ReflexBot extends Bot {
    ReflexBot() {}

    ReflexBot(int id) {
        this.id = id;
    }

    void move() {
        move_runner(false);
        move_blocker(false);
    }

    void move_as_main() {
        move_runner(true);
        move_blocker(true);
    }

    void move_runner(boolean for_output) {
        Pod pod = !for_output ? runner() : Globals.pods[0];

        Checkpoint cp = Globals.cps[pod.ncpid];
        Point t = new Point(cp.x - 3*pod.vx, cp.y - 3*pod.vy);
        double raw_angle = pod.diff_angle(t);

        int thrust = Math.abs(raw_angle) < 90 ? Globals.MAX_THRUST : 0;
        double angle = Math.max((double) -18, Math.min((double) 18, raw_angle));

        if (!for_output) pod.apply(thrust, angle);
        else Globals.print_move(thrust, angle, pod);
    }

    void move_blocker(boolean for_output) {
        Pod pod = !for_output ? blocker() : Globals.pods[1];

        Checkpoint cp = Globals.cps[pod.ncpid];
        Point t = new Point(cp.x - 3*pod.vx, cp.y - 3*pod.vy);
        double raw_angle = pod.diff_angle(t);

        int thrust = Math.abs(raw_angle) < 90 ? Globals.MAX_THRUST : 0;
        double angle = Math.max((double) -18, Math.min((double) 18, raw_angle));

        if (!for_output) pod.apply(thrust, angle);
        else Globals.print_move(thrust, angle, pod);
    }
};


// TODO
class SearchBot extends Bot {
    Solution sol;
    Bot[] oppBots;

    SearchBot() {}

    SearchBot(int id) {
        this.id = id;
    }

    void move(Solution sol) {
        Globals.pods[id].apply(sol.thrusts[Globals.turn], sol.angles[Globals.turn]);
        Globals.pods[id+1].apply(sol.thrusts[Globals.turn+Globals.DEPTH], sol.angles[Globals.turn+Globals.DEPTH]);
    }

    void move() {
        move(sol);
    }

    void solve(double time, boolean with_seed) {
        Solution best = new Solution(false);
        if (with_seed) {
            best = sol;
            best.shift();
        } else {
            best.randomize();
            if (Globals.r == 0 && Globals.pods[id].dist(Globals.cps[1]) > 4000) best.thrusts[0] = 650;
        }
        get_score(best);

        Solution child = new Solution(false);
        while (Globals.TIME() < time) {
            best.mutate(child);
            if (get_score(child) > get_score(best)) best = child;
        }
        sol = best;
    }

    double get_score(Solution sol) {
        if (sol.score == -1) {
            double[] scores = new double[oppBots.length];
            for (int i = 0; i < oppBots.length; i++) {
                scores[i] = get_bot_score(sol, oppBots[i]);
            }

            sol.score = Arrays.stream(scores).min().getAsDouble();;
        }

        return sol.score;
    }

    double get_bot_score(Solution sol, Bot opp) {
        double score = 0;
        while (Globals.turn < Globals.DEPTH) {
            move(sol);
            opp.move();
            Player.play();
            if (Globals.turn == 0) score += 0.1*evaluate();
            Globals.turn++;
        }
        score += 0.9*evaluate();
        Player.load();

        if (Globals.r > 0) Globals.sols_ct++;

        return score;
    }

    double evaluate() {
        Pod my_runner = runner(Globals.pods[id], Globals.pods[id+1]);
        Pod my_blocker = blocker(Globals.pods[id], Globals.pods[id+1]);
        Pod opp_runner = runner(Globals.pods[(id+2) % 4], Globals.pods[(id+3) % 4]);
        Pod opp_blocker = blocker(Globals.pods[(id+2) % 4], Globals.pods[(id+3) % 4]);

        double score = my_runner.score() - opp_runner.score();
        // TODO maybe not a great idea? :)
        score -= my_blocker.dist(opp_runner);

        return score;
    }
};


class Player {
    public static void load() {
        for (int i = 0; i < 4; i++) Globals.pods[i].load();
        Globals.turn = 0;
    }

    // TODO
    public static void play() {
        double t = 0.0;
        while (t < 1.0) {
            Collision first_col = new Collision(null, null, -1);
            for (int i = 0; i < 4; i++) {
                for (int j = i + 1; j < 4; j++) {
                    double col_time = Globals.pods[i].collision_time(Globals.pods[j]);
                    if (col_time > -1 && col_time + t < 1.0 && (first_col.t == -1 || col_time < first_col.t)) {
                        first_col.a = Globals.pods[i];
                        first_col.b = Globals.pods[j];
                        first_col.t = col_time;
                    }
                }
    
                // TODO this is wasteful, get rid of it
                double col_time = Globals.pods[i].collision_time(Globals.cps[Globals.pods[i].ncpid]);
                if (col_time > -1 && col_time + t < 1.0 && (first_col.t == -1 || col_time < first_col.t)) {
                    first_col.a = Globals.pods[i];
                    first_col.b = Globals.cps[Globals.pods[i].ncpid];
                    first_col.t = col_time;
                }
            }
    
            if (first_col.t == -1) {
                for (int i = 0; i < 4; i++) {
                    Globals.pods[i].move(1.0 - t);
                }
                t = 1.0;
            } else {
                for (int i = 0; i < 4; i++) {
                    Globals.pods[i].move(first_col.t);
                }
    
                first_col.a.bounce(first_col.b);
                t += first_col.t;
            }
        }
    
        for (int i = 0; i < 4; i++) {
            Globals.pods[i].end();
        }
    }

    // TODO
    public static void print_move(int thrust, double angle, Pod pod) {
        double a = pod.angle + angle;
    
        if (a >= 360.0) {
            a = a - 360.0;
        } else if (a < 0.0) {
            a += 360.0;
        }
    
        a = a * Math.PI / 180.0;
        double px = pod.x + Math.cos(a) * 10000.0;
        double py = pod.y + Math.sin(a) * 10000.0;
    
        String word = "test";
        if (thrust == -1) {
            System.out.printf("%d %d SHIELD %s\n", (int) Math.round(px), (int) Math.round(py), word);
            pod.shield = 4;
        } else if (thrust == 650) {
            pod.has_boost = 0;
            System.out.printf("%d %d BOOST %s\n", (int) Math.round(px), (int) Math.round(py), word);
        } else {
            System.out.printf("%d %d %d %s\n", (int) Math.round(px), (int) Math.round(py), thrust, word);
        }
    }
    
    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);

        Globals.laps = in.nextInt();;
        Globals.cp_ct = in.nextInt();
        Globals.cps = new Checkpoint[Globals.cp_ct];
        
        for (int i = 0; i < Globals.cp_ct; i++) {
            int checkpointX = in.nextInt();
            int checkpointY = in.nextInt();
            Globals.cps[i] = new Checkpoint(i, checkpointX, checkpointY);
        }
        
        Globals.pods = new Pod[4];
        
        for (int i = 0; i < 4; i++) Globals.pods[i] = new Pod(i);
        
        Globals.pods[0].partner = Globals.pods[1];
        Globals.pods[1].partner = Globals.pods[0];
        Globals.pods[2].partner = Globals.pods[3];
        Globals.pods[3].partner = Globals.pods[2];
        
        ReflexBot me_reflex = new ReflexBot();

        SearchBot opp = new SearchBot(2);
        opp.oppBots = new Bot[1];
        opp.oppBots[0] = me_reflex;
    
        SearchBot me = new SearchBot();
        me.oppBots = new Bot[1];
        me.oppBots[0] = opp;
        
        while (true) {
            Globals.r++;
            
            for (int i = 0; i < 4; i++) {
                int x = in.nextInt(); // x position of your pod
                int y = in.nextInt(); // y position of your pod
                int vx = in.nextInt(); // x speed of your pod
                int vy = in.nextInt(); // y speed of your pod
                int angle = in.nextInt(); // angle of your pod
                int ncpid = in.nextInt(); // next check point id of your pod
                if (Globals.r == 0 && i > 1 && angle > -1) Globals.is_p2 = true;
                Globals.pods[i].update(x, y, vx, vy, angle, ncpid);
            }

            Globals.now = System.currentTimeMillis();
            
            double time_limit = Globals.r == 0 ? 1000 : 75;
            time_limit *= 0.95;
    
            // use this to test reflex bot behavior
            // me_reflex.move_as_main();
    
            opp.solve(time_limit * 0.15, false);
            me.solve(time_limit, Globals.r > 0);
    
            if (Globals.r > 0){
                System.err.printf("Avg iters: %s; Avg sims: %s", Globals.sols_ct / Globals.r, Globals.sols_ct*Globals.DEPTH / Globals.r);
            }
    
            print_move(me.sol.thrusts[0], me.sol.angles[0], Globals.pods[0]);
            print_move(me.sol.thrusts[Globals.DEPTH], me.sol.angles[Globals.DEPTH], Globals.pods[1]);
        }
    }
}