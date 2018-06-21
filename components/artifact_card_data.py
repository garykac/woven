# Artifact card data

# Text -> ASCII Art: http://patorjk.com/software/taag/#p=display&f=Rectangles&t=Monster

artifact_card_revision = 1

artifact_card_data = [

	{
		'ability': 'When in a Forest location, move to any location within that connected Forest',
		'action': 'Move into Forest',
	},
	{
		'ability': 'When in a Mountain location, move to any location within that connected Mountain',
		'action': 'Move into Mountain',
	},
	{
		'ability': 'You may cross Rivers',
		'action': 'If adjacent to Lake, move to any location adjacent to that Lake',
	},
	{
		'ability': 'When in a Forest location, you may drop a Tendril',
		'action': 'Move a TENDRIL you control in a Forest location to any other location in that connected Forest',
	},
	{
		'ability': 'When in a Mountain location, you may drop a Tendril',
		'action': 'Move a TENDRIL you control in a Mountain location to any other location in that connected Mountain',
	},
	{
		'ability': 'When adjacent to a River, you may drop a Tendril',
		'action': 'Move a TENDRIL you control that is adjacent to a River 5 spaces along that River',
	},
	{
		'ability': 'When in a Forest, any defensive shield is doubled',
		'action': 'If in Forest, remove 1 CHARGE from all players in a neighboring Forest location.',
	},
	{
		'ability': 'When in a Mountain, any defensive shield is doubled',
		'action': 'If in Mountain, remove 1 CHARGE from all players in a neighboring Mountain location.',
	},
	{
		'ability': 'Your tendrils in Forest locations cannot be destroyed by other players',
		'action': 'Move all TENDRILs you control in Forest locations 1 space within that connected Forest',
	},
	{
		'ability': 'Your tendrils in Mountain locations cannot be destroyed by other players',
		'action': 'Move all TENDRILs you control in Mountain locations 1 space within that connected Mountain',
	},

]
