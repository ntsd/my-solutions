import java.util.*;
import java.io.*;
import java.math.*;

class Piece {
    // 1 WHITE 0 BLACK
    int owner;
    Cell cell;

    Piece(int owner, Cell cell) {
        this.owner = owner;
        this.cell = cell;
    }

    public int getOwner() {
        return owner;
    }

    int getX() {
        return cell.x;
    }

    int getY() {
        return cell.y;
    }

    void flip() {
        this.owner ^= 1;
    }
}

class Cell {
    int x, y;
    Piece piece;

    Cell(int x, int y) {
        this.x = x;
        this.y = y;
        this.piece = null;
    }

    Piece placePiece(int owner) {
        this.piece = new Piece(owner, this);
        return this.piece;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public Piece getPiece() {
        return piece;
    }

    @Override
    public String toString() {
        return (char) (97 + x) + Integer.toString(y + 1);
    }
}

enum Direction {
    N(0, -1), NE(1, -1), E(1, 0), SE(1, 1), S(0, 1), SW(-1, 1), W(-1, 0), NW(-1, -1);

    int x, y;

    Direction(int x, int y) {
        this.x = x;
        this.y = y;
    }
}

class Board extends Game {
    int WIDTH = 8;
    int HEIGHT = 8;

    Cell[][] cells;
    List<Piece> pieces;
    int[] piecesCounter;
    // Adding this so I don't need to compute stuff twice, this is just for viewer.
    ArrayList<ArrayList<Piece>> flips;

    public Board() {
        cells = new Cell[HEIGHT][WIDTH];
        pieces = new ArrayList<>();
        piecesCounter = new int[2];
        flips = new ArrayList<>();

        for (int y = 0; y < HEIGHT; ++y) {
            for (int x = 0; x < WIDTH; ++x) {
                cells[y][x] = new Cell(x, y);
            }
        }
        setupBoard();
    }

    public Cell[][] getCells() {
        return cells;
    }

    public int getHEIGHT() {
        return HEIGHT;
    }

    public int getWIDTH() {
        return WIDTH;
    }

    public int[] getPiecesCounter() {
        return piecesCounter;
    }

    void setupBoard() {
        int half = HEIGHT / 2;
        for (int y = half - 1; y <= half; ++y) {
            for (int x = half - 1; x <= half; ++x) {
                Piece piece = cells[y][x].placePiece((x == y) ? 1 : 0);
                pieces.add(piece);
                ++piecesCounter[(x == y) ? 1 : 0];
            }
        }
    }

    public void applyAction(Cell cell, int player) {
        Piece piece = cell.placePiece(player);
        pieces.add(piece);
        ++piecesCounter[player];
        List<Piece> origins = new ArrayList<>();
        flips = new ArrayList<>();
        origins.add(piece);
        flip(origins);
    }

    void flip(List<Piece> origins) {
        List<Piece> toFlip = new ArrayList<>();
        for (Piece piece : origins) {
            for (Direction dir : Direction.values()) {
                List<Piece> piecesToAdd = new ArrayList<>();
                int x = piece.getX();
                int y = piece.getY();

                while (true) {
                    x += dir.x;
                    y += dir.y;
                    if (x < 0 || x > WIDTH - 1)
                        break;
                    if (y < 0 || y > HEIGHT - 1)
                        break;

                    Cell cell = cells[y][x];
                    if (cell.piece == null) {
                        break;
                    } else {
                        // Can only jump over opponent pieces
                        if (cell.piece.owner != piece.owner) {
                            piecesToAdd.add(cell.piece);
                        } else {
                            for (Piece p : piecesToAdd) {
                                if (!toFlip.contains(p))
                                    toFlip.add(p);
                            }

                            if (piecesToAdd.size() > 0) {
                                flips.add(new ArrayList());
                                flips.get(flips.size() - 1).addAll(piecesToAdd);
                            }

                            break;
                        }
                    }
                }
            }
        }

        for (Piece piece : toFlip) {
            --piecesCounter[piece.owner];
            piece.flip();
            ++piecesCounter[piece.owner];
        }
    }

    public List<Cell> getActions(int player) {
        List<Cell> actions = new ArrayList<>();

        for (Piece piece : pieces) {
            if (piece.owner != player)
                continue;

            for (Direction dir : Direction.values()) {
                int count = 0;
                int x = piece.getX();
                int y = piece.getY();
                while (true) {
                    x += dir.x;
                    y += dir.y;

                    if (x < 0 || x > WIDTH - 1)
                        break;
                    if (y < 0 || y > HEIGHT - 1)
                        break;

                    Cell cell = cells[y][x];

                    if (cell.piece == null) {
                        if (count > 0) {
                            // ADD ACTION
                            if (!actions.contains(cell))
                                actions.add(cell);
                        }
                        break;
                    } else {
                        // Can only jump over opponent pieces
                        if (cell.piece.owner != player) {
                            count++;
                        } else {
                            break;
                        }
                    }
                }
            }
        }

        return actions;
    }

    public int getState(Cell[][]> board) {
        
    }
}

public abstract class Game {
    
    public Cell[][] board_state; //index(0) = player to move;

    public abstract List<Cell> legalMoves(Cell[][] board);

    public abstract int makeMove(Cell m); //returns 0 if game is not over, returns player who won, -1 if illegal move

    public abstract int simMove(Cell m, Cell[][] board); //same as above except operates on board, returns victory state
    
    public abstract int getState(Cell[][] board); //-2 for draw, 0 for not over, else winning player
}

class Node {

    byte move;
    int wins;
    Node parent;
    ArrayList<Node> children;
    long sims;
    ArrayList<Byte> state;
    int finished = 0; // 0 = not fininshed, otherwise equals winner

    public Node(Node parent, ArrayList<Byte> state, byte move) {
        this.parent = parent;
        this.state = state;
        this.move = move;
        children = new ArrayList<>();
    }
}

class MCTS {

    final int branch = 100; //set to max
    final double epsilon = 1e-5;
    int playouts;
    Game game;
    int player;
    Node start;

    public MCTS(Game game, int player, ArrayList<Byte> state, int playouts){
        this.playouts = playouts;
        this.game = game;
        this.player = player;
        start = new Node(null, state, (byte)-1);
    }

    public byte getMove() {
        byte move = start.children.get(0).move;
        long high = -2;
        for (int j = 0; j < start.children.size(); j++) {
            Node n = start.children.get(j);
            if (n.finished == player) {
                return n.move;
            } else if (n.finished == 0 && n.sims > high) {
                high = n.sims;
                move = n.move;
            } else if (n.finished == 3 && -1 > high) { //can draw
                high = -1;
                move = n.move;
            }
        }
        return move;
    }

    public boolean round() { //returns solved
        if (start.finished != 0) {
            System.err.print("(SOLVED FOR: " + start.finished+") " + start.children.size() + ":");
            return true;
        }
        Node n = selection();

        if (n == null) { //solved the game?
            //System.out.println("SOLVED");
            //return true;
            return false;
        }

        Node leaf = expansion(n);
        if (leaf == null) {
            leaf = n;
            //System.out.println("Reached Leaf");
        }

        for (int j = 0; j < playouts; j++) {
            int result = simulation(leaf);

            if (leaf == n) {

                if (result == -2) {
                    result = 3;
                }
                if(n.parent != null) n.parent.finished = result;
                n.finished = result;
                j = playouts;
            }

            Node p = leaf;
            while (p != null) {
                if (result == player) {
                    p.wins++;
                }
                p.sims++;
                p = p.parent;
            }
        }  
        return false;
    }

    public Node selection() { //select a leaf node return index

        Node s = start;
        while (s.children.size() != 0) {
            int index = -1;
            double high = -2;
            int sumfinished = 0;
            int finishedtype = -1;
            for (int j = 0; j < s.children.size(); j++) {
                Node n = s.children.get(j);

                long wins = n.wins;
                if (s.state.get(0) != player) {
                    wins = n.sims - n.wins;//opponents move
                }
                if (n.finished == 0) {
                    double ucb = wins / (n.sims + epsilon) + Math.sqrt((Math.log(s.sims + 2) / (n.sims + epsilon)));
                    if (ucb > high) {
                        high = ucb;
                        index = j;
                    }
                } else {
                    if (finishedtype == -1) {
                        finishedtype = n.finished;
                        sumfinished += n.finished;
                        if (n.finished == s.state.get(0)) {
                            //index = j;
                            //high = Double.POSITIVE_INFINITY;
                            s.finished = n.finished;
                            return null;
                        } else if (n.finished == 3 && -1 > high) {
                            high = -1;
                            index = j;
                        }
                    } else if (finishedtype == n.finished) {
                        sumfinished += n.finished;

                    } else {
                        finishedtype = -2;
                        sumfinished = 0;
                        if (n.finished == s.state.get(0)) {
                            //index = j;
                            //high = Double.POSITIVE_INFINITY;
                            s.finished = n.finished;
                            return null;
                        } else if (n.finished == 3 && -1 > high) {
                            high = -1;
                            index = j;
                        }
                    }

                }
            }
            int opp = 2;
            if (s.state.get(0) == 2) {
                opp = 1;
            }
            if (finishedtype == opp && sumfinished == s.children.size() * opp) {
                s.finished = opp;
                return null;
            } else if (high == -1) { //best case draw
                s.finished = 3;
                return null;
            } else if (index != -1) {
                s = s.children.get(index);
            } else if (index == -1) {
                System.out.println("SOMETHINGS WRONG");
                return null;
            }
        }
        return s;
    }

    public Node expansion(Node n) { // choose child of leaf node

        ArrayList<Byte> moves = game.legalMoves(n.state);
        Node c = null;
        int index;
        while (!moves.isEmpty() && n.children.size() < branch) {
            index = (int) (Math.random() * moves.size());
            ArrayList<Byte> state = new ArrayList<>(n.state.size());
            for (Byte i : n.state) {
                state.add(i);
            }
            game.simMove(moves.get(index), state);
            c = new Node(n, state, moves.get(index));
            n.children.add(c);
            moves.remove(index);
            //nodes.add(c);
        }
        
        if (c == null) {
            return null;
        }
        return c;
    }

    public int simulation(Node n) { //random playout until end, returns player who won, -1 for draw
        int result = result = game.getState(n.state);
        if (result != 0) {
            return result;
        }
        ArrayList<Byte> board = new ArrayList<>(n.state.size());
        for (Byte i : n.state) {
            board.add(i);
        }
        ArrayList<Byte> moves;

        while (result == 0) {
            moves = game.legalMoves(board);
            if (moves.isEmpty()) {
                return -1;
            }
            result = game.simMove(moves.get((int) (Math.random() * moves.size())), board);
        }
        return result;
    }
}

class Player {
    static Random rand = new Random();

    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);

        int id = in.nextInt(); // id of your player.
        int boardSize = in.nextInt();

        Board board = new Board();
        board.setupBoard();

        while (true) {
            for (int i = 0; i < boardSize; i++) {
                String line = in.next(); // rows from top to bottom (viewer perspective).
            }

            List<String> actionList = new ArrayList<String>();

            int actionCount = in.nextInt();
            for (int i = 0; i < actionCount; i++) {
                String action = in.next();
                actionList.add(action);
            }

            System.out.println(actionList.get(rand.nextInt(actionCount))); // a-h1-8
        }
    }
}
