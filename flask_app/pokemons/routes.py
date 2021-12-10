from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from flask_mail import Mail, Message
from .. import mail

from .. import poke_client
from ..forms import PokeReviewForm, SearchForm, PokeInputForm
from ..models import User, Review
from ..utils import current_time

pokemons = Blueprint('pokemons', __name__)

# search on the first page
@pokemons.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("pokemons.query_results", query=form.search_query.data))

    input_form = PokeInputForm()

    if input_form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=input_form.text.data,
            date=current_time(),
            poke_name="General",
        )
        review.save()

        msg = Message("You just submitted a review.",
              recipients=[current_user.email])

        msg.body = "This is your submitted review for Pokemon in general: " + str(input_form.text.data)
    
        mail.send(msg) 

        return redirect(request.path)

    reviews = Review.objects(poke_name="General")

    return render_template("index.html", form=form, input_form=input_form, reviews=reviews)

# gathers results from search
@pokemons.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = poke_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)

@pokemons.route("/about")
def about():
    return render_template("about.html")

# displays pokemon info
@pokemons.route('/pokemon/<pokemon_name>', methods=["GET", "POST"])
def pokemon_info(pokemon_name):

    poke_dict = poke_client.get_pokemon_info(pokemon_name)

    form = PokeReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            poke_name=pokemon_name,
        )

        review.save()

        msg = Message("You just submitted a review.",
              recipients=[current_user.email])

        msg.body = "This is your submitted review for " + str(pokemon_name) + ": " + str(form.text.data)
    
        mail.send(msg) 

        return redirect(request.path)

    reviews = Review.objects(poke_name=pokemon_name)

    return render_template("pokemon.html", form=form, pokemon_name=pokemon_name, reviews=reviews, poke_dict=poke_dict)


# not sure if we need. but won't hurt to have for now
@pokemons.route('/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    """
    Must show a list of pokemon 

    Check the README for more detail
    """
    poke_w_ability_list = poke_client.get_pokemon_with_ability(ability_name)
    return render_template('ability.html', ability=ability_name, poke_w_ability_list=poke_w_ability_list)

@pokemons.route("/user/<username>")
def user_detail(username):
    
    user = User.objects(username=username).first()
    try:
        reviews = Review.objects(commenter=user)
    except ValueError as e:
        return render_template("user_detail.html", error_msg=str(e))

    return render_template("user_detail.html", reviews=reviews, username=username)