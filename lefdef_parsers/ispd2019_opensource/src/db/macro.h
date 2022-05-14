#ifndef _DB_MACRO_H_
#define _DB_MACRO_H_

namespace ispd19 {

class Pin;

class Macro
{
public:
    static const unsigned NullIndex = UINT_MAX;
    Macro() { }
    Macro(const std::string &n) : _name(n) { }
    const std::string& name() const { return _name; }
    void name( const std::string &n ) { _name = n; }
    const std::string& cls() const { return _class; }
    void cls( const std::string &c ) { _class = c; }
    const std::string& site() const { return _site; }
    void site( const std::string &s ) { _site = s; }

    int width() const { return _size.width(); }
    int height() const { return _size.height(); }
    void size(int origX, int origY, int width, int height) {
        _size.lx(origX);
        _size.ly(origY);
        _size.hx(origX + width);
        _size.hy(origY + height);
    }

    Pin& addPin(const std::string &n) {
        _pins.emplace_back(n);
        return _pins.back();
    }

    void report() const {
        std::cout<<_name<<std::endl;
        std::cout<<"--pins("<<_pins.size()<<")"<<std::endl;
        for( const Pin &pin : _pins )
        {
            pin.report();
        }
    }

private:
    std::string _name;
    std::string _class;
    std::string _site;
    Box _size;
    std::vector<Pin> _pins;
};

}

#endif

