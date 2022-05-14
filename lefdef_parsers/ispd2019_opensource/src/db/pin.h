#ifndef _DB_PIN_H_
#define _DB_PIN_H_

namespace ispd19 {

class Pin
{
public:
    Pin() { }
    Pin(const std::string &n) : _name( n ) { }
    const std::string& name() const { return _name; }
    bool isUseAnalog() const { return _use == 'a'; }
    bool isUseClock() const { return _use == 'c'; }
    bool isUseGround() const { return _use == 'g'; }
    bool isUsePower() const { return _use == 'p'; }
    bool isUseSignal() const { return _use == 's'; }
    void setIsUseAnalog() { _use = 'a'; }
    void setIsUseClock() { _use = 'c'; }
    void setIsUseGround() { _use = 'g'; }
    void setIsUsePower() { _use = 'p'; }
    void setIsUseSignal() { _use = 's'; }

    bool isInput() const { return _dir == 'i'; }
    bool isOutput() const { return _dir == 'o'; }
    bool isInOut() const { return _dir == 'b'; }
    void setIsInput() { _dir = 'i'; }
    void setIsOutput() { _dir = 'o'; }
    void setIsInOut() { _dir = 'b'; }
    void addShape(int lx, int ly, int hx, int hy, unsigned char z) {
        _shapes.emplace_back(lx, ly, hx, hy, z);
        if( _box == Box::Null ) {
            _box == _shapes.back().box();
        }
        _box.merge(_shapes.back().box());
    }
    bool inside(const Point &pt);
    void report() const {
        std::cout<<_name<<std::endl;
        std::cout<<"use : "<<_use<<std::endl;
        std::cout<<"dir : "<<_dir<<std::endl;
        std::cout<<"shape : "<<std::endl;
        for( const Shape &shape : _shapes )
        {
            std::cout<<shape.toString()<<std::endl;
        }
    }
private:
    std::string _name;
    std::vector<Shape> _shapes;
    Box _box;
    char _direction;
    char _use;
    char _dir;
};

}

#endif

