import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


#Setting up pagination
QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
   page = request.args.get('page', 1, type=int)
   start = (page - 1) * QUESTIONS_PER_PAGE
   end = start + QUESTIONS_PER_PAGE

   questions = [questions.format() for item in selection]
   current_questions =questions[start:end]

   return current_questions


def create_app(test_config=None):
    app=Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request( response ):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, POST, POST, DELETE, OPTIONS')
      return response 


        # an endpoint to handle `GET` requests for questions including pagination 
        # (every 10 questions). This endpoint should return a list of questions, 
        # number of total questions, current category, categories.

    @app.route('/questions', methods=['GET'])
    def get_questions():
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection) 

      if current_questions is None:
        abort(404)

      else:
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all())
            })


        # setting up an endpoint to handle `GET` requests for all available categories

    @app.route('/categories', methods=['GET'])
    def get_categories():
      Categories = Category.query.all()
      formatted_Categories = [Categories.format() for category in Categories] 

      if Category is None:
        abort(404)

      else:
        return jsonify({
            'success': True,
            'questions': formatted_Categories
        })

        # setting an endpoint to `DELETE` a question using a question `ID`

        @app.route('/questions/<int:question_id>', methods=['DELETE'])
        def delete_question(question_id):
          try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
            'success': True,
            'questions': current_questions,
            'deleted': question_id,
            'total_questions': len(Question.query.all())
            })

          except:
            abort(422)

        # setting up an endpoint to `POST` a new question, which will require the 
        # question and answer text, category, and difficulty score

        @app.route('/questions', methods=['POST'])
        def post_questions():
          body = request.get_json()

          new_question = body.get('question_text', None)
          new_answer = body.get('answer_text', None)
          category = body.get('category', None)
          difficulty = body.get('difficulty_level', None)

          try:
            question = Question(new_question=question_text, new_answer=answer_text, category=category, difficulty=difficulty_level)
            current_questions = paginate_questions(request, selection)

            return jsonify({
            'success': True,
            'questions': current_questions,
            'created': question_id,
            'total_questions': len(Question.query.all())
            })

          except:
            abort(422)

        # setting up a `POST` endpoint to get questions based on category.

        @app.route('/questions', methods=['POST'])
        def post_questions_by_category(category_id):

          try:
            questions = Question.query.filter(Question.category == str(category_id)).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
            'success': True,
            'questions': current_questions,
            'category': category_id,
            'total_questions': len(Question.query.all())
            })

          except:
            abort(422)

        #setting up a `POST` endpoint to get questions based on a search term

        @app.route('/questions/search', methods=['POST'])
        def post_questions_by_search_term():
            body = request.get_json()
            search_term = body.get('searchTerm', None)
        
        if search_term:
            search_results = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()
            
        return jsonify({
            'success': True,
            'questions': [question.format() for question in search_results],
            'total_questions': len(search_results),
            'current_category': None
        })

        abort(404)

        #setting up a `POST` endpoint to get questions to play the quiz

        @app.route('/quizzes', methods=[POST])
        def post_quizzes():
        
          try:
            body = request.get_json()
            
            if not ('quiz_category'in body and 'previous_questions' in body):
                abort(422)
                
            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')
            
            if category['type'] == 'click':
                current_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                current_questions = Question.query.filter.by(
                    category=category['id']).filter(Question.id.notin_((previous_questions))).all()
                    
                    
            new_question = available_questions[random.randrange(
                0, len(available_available))].format() if len(available_questions) > 0 else None
            
            return jsonify({
                'success': True,
                'question': new_question
            })
          except:
            abort(422)

        return app