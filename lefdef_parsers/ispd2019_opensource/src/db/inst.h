#ifndef _DB_INST_H_
#define _DB_INST_H_

namespace ispd19 {

class Pin;

class Instance
{
public:
    static const unsigned NullIndex = UINT_MAX;
    Instance() { }
    Instance(const std::string &name) :
        _name( name ) { }
    void place(int ix, int iy, bool fx, bool fy){
        _loc.x(ix);
        _loc.y(iy);
        _flipX = fx;
        _flipY = fy;
    }
    void unplace() {
        _loc = Point::Null;
        _flipX = false;
        _flipY = false;
    }
    bool isPlaced() const { return _loc == Point::Null; }
    int x() const { return _loc.x(); }
    int y() const { return _loc.y(); }
    unsigned macro() const { return _macro; }
    void macro(unsigned m) { _macro = m; }
private:
    std::string _name;
    unsigned _macro;
    Point _loc;
    bool _flipX;
    bool _flipY;
    std::vector<Pin*> _pins;
};

}

#endif

