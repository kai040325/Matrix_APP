from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from fractions import Fraction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matrix.db'
db = SQLAlchemy(app)

class Matrix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matrix_1_1 = db.Column(db.Integer, nullable=False)
    matrix_1_2 = db.Column(db.Integer, nullable=False)
    matrix_1_3 = db.Column(db.Integer, nullable=False)
    matrix_2_1 = db.Column(db.Integer, nullable=False)
    matrix_2_2 = db.Column(db.Integer, nullable=False)
    matrix_2_3 = db.Column(db.Integer, nullable=False)
    matrix_3_1 = db.Column(db.Integer, nullable=False)
    matrix_3_2 = db.Column(db.Integer, nullable=False)
    matrix_3_3 = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    return render_template('calculation.html')

@app.route("/result", methods=["GET","POST"])
def result():
    if request.method == "GET":
        return render_template("calculation.html")
    else:
        matrix_1_1 = request.form.get("matrix_1_1")
        matrix_1_2 = request.form.get("matrix_1_2")
        matrix_1_3 = request.form.get("matrix_1_3")
        matrix_2_1 = request.form.get("matrix_2_1")
        matrix_2_2 = request.form.get("matrix_2_2")
        matrix_2_3 = request.form.get("matrix_2_3")
        matrix_3_1 = request.form.get("matrix_3_1")
        matrix_3_2 = request.form.get("matrix_3_2")
        matrix_3_3 = request.form.get("matrix_3_3")
        
        matrix_list = [[matrix_1_1,matrix_1_2,matrix_1_3],
                       [matrix_2_1,matrix_2_2,matrix_2_3],
                       [matrix_3_1,matrix_3_2,matrix_3_3]]
        
        for matrix_line_number in range(len(matrix_list)):
            for matrix_line_row_number in range(len(matrix_list[matrix_line_number])):
                if "/" in str(matrix_list[matrix_line_number][matrix_line_row_number]):
                    matrix_line_row_fraction = (str(matrix_list[matrix_line_number][matrix_line_row_number])).split("/")
                    matrix_line_row_fraction_numerator = int(matrix_line_row_fraction[0])
                    matrix_line_row_fraction_denominator = int(matrix_line_row_fraction[1])
                    matrix_list[matrix_line_number][matrix_line_row_number] = Fraction(matrix_line_row_fraction_numerator,matrix_line_row_fraction_denominator)
                else:
                    matrix_list[matrix_line_number][matrix_line_row_number] = int(matrix_list[matrix_line_number][matrix_line_row_number])
            
        determinant = matrix_list[0][0] * matrix_list[1][1] * matrix_list[2][2] + matrix_list[0][1] * matrix_list[1][2] * matrix_list[2][0] + matrix_list[0][2] * matrix_list[1][0] * matrix_list[2][1] - matrix_list[0][2] * matrix_list[1][1] * matrix_list[2][0] - matrix_list[0][1] * matrix_list[1][0] * matrix_list[2][2] - matrix_list[0][0] * matrix_list[1][2] * matrix_list[2][1]
        
        if determinant == 0:
            error_message = "行列式が０のため逆行列は存在しません"
            return render_template("result.html", error_message=error_message)
        else:
            result_matrix_1_1 = Fraction(((matrix_list[1][1] * matrix_list[2][2] )- (matrix_list[1][2] * matrix_list[2][1])),determinant)
            result_matrix_1_2 = Fraction(-((matrix_list[0][1] * matrix_list[2][2] )- (matrix_list[0][2] * matrix_list[2][1])),determinant)
            result_matrix_1_3 = Fraction(((matrix_list[0][1] * matrix_list[1][2] )- (matrix_list[0][2] * matrix_list[1][1])),determinant)
            result_matrix_2_1 = Fraction(-((matrix_list[1][0] * matrix_list[2][2] )- (matrix_list[1][2] * matrix_list[2][0])),determinant)
            result_matrix_2_2 = Fraction(((matrix_list[0][0] * matrix_list[2][2] )- (matrix_list[0][2] * matrix_list[2][0])),determinant)
            result_matrix_2_3 = Fraction(-((matrix_list[0][0] * matrix_list[1][2] )- (matrix_list[0][2] * matrix_list[1][0])),determinant)
            result_matrix_3_1 = Fraction(((matrix_list[1][0] * matrix_list[2][1] )- (matrix_list[1][1] * matrix_list[2][0])),determinant)
            result_matrix_3_2 = Fraction(-((matrix_list[0][0] * matrix_list[2][2] )- (matrix_list[0][2] * matrix_list[2][0])),determinant)
            result_matrix_3_3 = Fraction(((matrix_list[0][0] * matrix_list[1][2] )- (matrix_list[0][2] * matrix_list[1][0])),determinant)
            

        return render_template("result.html",result_matrix_1_1=result_matrix_1_1,result_matrix_1_2=result_matrix_1_2,result_matrix_1_3=result_matrix_1_3,result_matrix_2_1=result_matrix_2_1,result_matrix_2_2=result_matrix_2_2,result_matrix_2_3=result_matrix_2_3,result_matrix_3_1=result_matrix_3_1,result_matrix_3_2=result_matrix_3_2,result_matrix_3_3=result_matrix_3_3,matrix_1_1=matrix_1_1,matrix_1_2=matrix_1_2,matrix_1_3=matrix_1_3,matrix_2_1=matrix_2_1,matrix_2_2=matrix_2_2,matrix_2_3=matrix_2_3,matrix_3_1=matrix_3_1,matrix_3_2=matrix_3_2,matrix_3_3=matrix_3_3)
        

        
if __name__ == '__main__':
    app.run(debug=True)

