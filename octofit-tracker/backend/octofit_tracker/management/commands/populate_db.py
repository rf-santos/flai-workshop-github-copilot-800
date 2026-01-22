from django.core.management.base import BaseCommand
from django.utils import timezone
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes unite for fitness!',
            captain='Iron Man',
            members_count=6,
            total_points=0
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League assembles for ultimate fitness!',
            captain='Superman',
            members_count=6,
            total_points=0
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Team.objects.count()} teams'))
        
        # Create Users
        self.stdout.write('Creating users...')
        
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@avengers.com', 'avatar': 'https://i.pravatar.cc/150?img=1'},
            {'name': 'Captain America', 'email': 'steve.rogers@avengers.com', 'avatar': 'https://i.pravatar.cc/150?img=2'},
            {'name': 'Thor', 'email': 'thor.odinson@avengers.com', 'avatar': 'https://i.pravatar.cc/150?img=3'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@avengers.com', 'avatar': 'https://i.pravatar.cc/150?img=4'},
            {'name': 'Hulk', 'email': 'bruce.banner@avengers.com', 'avatar': 'https://i.pravatar.cc/150?img=5'},
            {'name': 'Spider-Man', 'email': 'peter.parker@avengers.com', 'avatar': 'https://i.pravatar.cc/150?img=6'},
        ]
        
        dc_heroes = [
            {'name': 'Superman', 'email': 'clark.kent@justiceleague.com', 'avatar': 'https://i.pravatar.cc/150?img=7'},
            {'name': 'Batman', 'email': 'bruce.wayne@justiceleague.com', 'avatar': 'https://i.pravatar.cc/150?img=8'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@justiceleague.com', 'avatar': 'https://i.pravatar.cc/150?img=9'},
            {'name': 'Flash', 'email': 'barry.allen@justiceleague.com', 'avatar': 'https://i.pravatar.cc/150?img=10'},
            {'name': 'Aquaman', 'email': 'arthur.curry@justiceleague.com', 'avatar': 'https://i.pravatar.cc/150?img=11'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@justiceleague.com', 'avatar': 'https://i.pravatar.cc/150?img=12'},
        ]
        
        users = []
        for hero in marvel_heroes:
            users.append(User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team='Team Marvel',
                avatar=hero['avatar']
            ))
        
        for hero in dc_heroes:
            users.append(User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team='Team DC',
                avatar=hero['avatar']
            ))
        
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.count()} users'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'Hiking']
        
        activities = []
        team_points = {'Team Marvel': 0, 'Team DC': 0}
        
        for user in users:
            # Create 3-7 activities per user
            num_activities = random.randint(3, 7)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = round(random.uniform(2.0, 20.0), 2) if activity_type in ['Running', 'Cycling', 'Swimming', 'Hiking'] else 0.0
                calories = duration * random.randint(5, 12)
                points = duration + (int(distance) * 10) + (calories // 10)
                
                activity_date = timezone.now() - timedelta(days=random.randint(0, 30))
                
                activities.append(Activity.objects.create(
                    user_id=str(user._id),
                    user_name=user.name,
                    team=user.team,
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    points=points,
                    date=activity_date
                ))
                
                team_points[user.team] += points
        
        self.stdout.write(self.style.SUCCESS(f'Created {Activity.objects.count()} activities'))
        
        # Update team points
        team_marvel.total_points = team_points['Team Marvel']
        team_marvel.save()
        
        team_dc.total_points = team_points['Team DC']
        team_dc.save()
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        
        teams_data = [
            {'team': 'Team Marvel', 'points': team_points['Team Marvel']},
            {'team': 'Team DC', 'points': team_points['Team DC']},
        ]
        
        # Sort teams by points to assign ranks
        teams_data.sort(key=lambda x: x['points'], reverse=True)
        
        for rank, team_data in enumerate(teams_data, 1):
            team_name = team_data['team']
            team_activities = Activity.objects.filter(team=team_name)
            
            total_activities = team_activities.count()
            total_calories = sum(a.calories for a in team_activities)
            total_distance = sum(a.distance for a in team_activities)
            
            Leaderboard.objects.create(
                team=team_name,
                total_points=team_data['points'],
                total_activities=total_activities,
                total_calories=total_calories,
                total_distance=total_distance,
                rank=rank
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {Leaderboard.objects.count()} leaderboard entries'))
        
        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        
        workouts_data = [
            {
                'name': 'Super Soldier Training',
                'description': 'Captain America\'s legendary workout routine for peak physical condition',
                'activity_type': 'Weightlifting',
                'difficulty': 'advanced',
                'duration': 60,
                'calories_estimate': 500,
                'instructions': [
                    'Warm-up: 10 minutes of light cardio',
                    'Bench press: 4 sets of 10 reps',
                    'Pull-ups: 4 sets of 12 reps',
                    'Squats: 4 sets of 15 reps',
                    'Deadlifts: 3 sets of 8 reps',
                    'Cool-down: 10 minutes of stretching'
                ]
            },
            {
                'name': 'Speed Force Sprint',
                'description': 'Flash-inspired interval running for maximum speed and endurance',
                'activity_type': 'Running',
                'difficulty': 'intermediate',
                'duration': 45,
                'calories_estimate': 450,
                'instructions': [
                    'Warm-up: 5 minutes of jogging',
                    'Sprint: 30 seconds at maximum speed',
                    'Recovery jog: 90 seconds',
                    'Repeat sprint/recovery 10 times',
                    'Cool-down: 5 minutes of walking'
                ]
            },
            {
                'name': 'Asgardian Power Lift',
                'description': 'Thor\'s mighty strength training routine',
                'activity_type': 'Weightlifting',
                'difficulty': 'advanced',
                'duration': 75,
                'calories_estimate': 600,
                'instructions': [
                    'Hammer lifts: 5 sets of 5 reps',
                    'Overhead press: 4 sets of 8 reps',
                    'Battle rope waves: 3 sets of 30 seconds',
                    'Farmer\'s walk: 4 sets of 50 meters',
                    'Core work: 3 sets of planks'
                ]
            },
            {
                'name': 'Amazonian Warrior Flow',
                'description': 'Wonder Woman\'s balanced yoga and strength routine',
                'activity_type': 'Yoga',
                'difficulty': 'intermediate',
                'duration': 50,
                'calories_estimate': 300,
                'instructions': [
                    'Sun salutations: 5 rounds',
                    'Warrior poses: hold each for 60 seconds',
                    'Balance poses: tree and eagle',
                    'Core strengthening: boat pose series',
                    'Meditation: 10 minutes'
                ]
            },
            {
                'name': 'Batcave Boxing Circuit',
                'description': 'Batman\'s intense boxing and cardio workout',
                'activity_type': 'Boxing',
                'difficulty': 'advanced',
                'duration': 60,
                'calories_estimate': 550,
                'instructions': [
                    'Jump rope: 5 minutes',
                    'Heavy bag: 3 rounds of 3 minutes',
                    'Speed bag: 3 rounds of 2 minutes',
                    'Shadow boxing: 3 rounds of 3 minutes',
                    'Core circuit: 15 minutes'
                ]
            },
            {
                'name': 'Atlantean Swimming Challenge',
                'description': 'Aquaman\'s oceanic endurance swim workout',
                'activity_type': 'Swimming',
                'difficulty': 'intermediate',
                'duration': 45,
                'calories_estimate': 400,
                'instructions': [
                    'Warm-up: 200m easy swim',
                    'Freestyle: 8 x 100m intervals',
                    'Backstroke: 4 x 50m',
                    'Butterfly: 4 x 25m sprints',
                    'Cool-down: 200m easy swim'
                ]
            },
            {
                'name': 'Web-Slinger Mobility',
                'description': 'Spider-Man\'s agility and flexibility routine',
                'activity_type': 'Yoga',
                'difficulty': 'beginner',
                'duration': 30,
                'calories_estimate': 200,
                'instructions': [
                    'Dynamic stretching: 10 minutes',
                    'Spider stretch: 3 sets of 30 seconds',
                    'Leg swings and arm circles',
                    'Balance work: single leg holds',
                    'Cool-down stretches'
                ]
            },
            {
                'name': 'Kryptonian Mountain Trek',
                'description': 'Superman\'s high-altitude hiking workout',
                'activity_type': 'Hiking',
                'difficulty': 'intermediate',
                'duration': 90,
                'calories_estimate': 650,
                'instructions': [
                    'Start with steady uphill pace',
                    'Maintain consistent breathing',
                    'Take short breaks every 15 minutes',
                    'Use trekking poles for stability',
                    'Descend carefully with controlled steps'
                ]
            }
        ]
        
        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Workout.objects.count()} workout suggestions'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'\nTeam Marvel Points: {team_points["Team Marvel"]}'))
        self.stdout.write(self.style.SUCCESS(f'Team DC Points: {team_points["Team DC"]}'))
