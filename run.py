from src.app import app


if __name__ == "__main__":
    '''
    db.create_all()
    hased = sha256_crypt.encrypt('nocap')
    db.session.add(Admin(username="Iyera david", password=hased))
    db.session.commit()'''
    app.run(debug=True)